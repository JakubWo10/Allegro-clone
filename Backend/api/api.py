from datetime import datetime, timedelta, timezone
from typing import Callable, Dict

import jwt
from api.api_models.Google import GoogleToken
from api.api_models.Product import ProductOut
from api.api_models.User import Reguser, UserOut
from api.UserService import UserService
from config.config import AVATARS_DIR, PRODUCTS_DIR, settings
from database.DataClient import create_database_client
from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Security,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from fastapi.staticfiles import StaticFiles
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import ExpiredSignatureError
from jwt import PyJWTError
from passlib.context import CryptContext
from transform.Transform import Transform

from .exceptions import MyHttpException

transformer = Transform()
data_client = create_database_client(settings.DATABASE_URL)
User_service = UserService(DATA_CLIENT=data_client, TRANSFORM=transformer)


app = FastAPI()

app.mount("/avatars", StaticFiles(directory=AVATARS_DIR), name="avatars")
app.mount("/products", StaticFiles(directory=PRODUCTS_DIR), name="products")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scopes={"user": "Basic user role permissions /me, /addproduct /changepicture", "admin": "Manages the entire appliaction", "test": "useless scope for testing"},
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def get_user_service() -> UserService:
    return User_service


def create_token(username: str, user_id: str, user_scope: str) -> str:
    if user_scope == "admin":
        scopes = ["user", "admin"]
    else:
        scopes = ["user"]
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRES)
    payload = {"sub": username, "exp": exp_date, "user_id": user_id, "scopes": scopes}
    return jwt.encode(payload, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)


async def verify_token(token: str, security_scopes) -> Dict[str, str] | bool:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.INVALID_TOKEN,
        )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        username = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=MyHttpException.UNAUTHORIZED,
            )
        exist = await User_service.user_exist_all_data(username)
        if not exist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=MyHttpException.UNAUTHORIZED,
            )

        for scope in security_scopes.scopes:  # ["user"]
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=MyHttpException.UNAUTHORIZED,
                )
    except (PyJWTError, ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.INVALID_TOKEN,
        )
    return exist


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> Dict[str, str] | bool:
    user = await verify_token(token, security_scopes)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MyHttpException.UNAUTHORIZED)

    return user


@app.post("/register")
async def register(reg_user: Reguser, service: UserService = Depends(get_user_service)) -> Dict[str, str]:
    user_name = reg_user.name

    exist = await service.user_name_exist(user_name)

    if exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MyHttpException.NAME_IS_TAKEN)

    user_password_hashed = hash_password(reg_user.password)
    user = service.create_user(user_password_hashed, "user", reg_user)
    response = await service.insert_user(user)

    if response:
        return {"detail": "Sucessful register"}

    return {"detail": "Something went wrong"}


@app.post("/Google/login")  # TOO LONG ENDPOINT HAVE TO REFRACTOR THIS CODE
async def login_google(google_token: GoogleToken, service: UserService = Depends(get_user_service)):

    try:
        id_info = id_token.verify_oauth2_token(google_token.google_token, requests.Request(), settings.VITE_GOOGLE_CLIENT_ID.get_secret_value())

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidłowy token Google")

    user_email = id_info.get("email")
    username = id_info.get("name")
    user_google_id = id_info.get("sub")

    result = await service.user_name_exist(username)

    if not result:

        Google_user = service.transform_to_google_user(username, user_email, user_google_id, "user")

        await service.insert_user(Google_user)
        user = await service.user_name_exist(username)

        user_google_picture_link = id_info.get("picture")

        if isinstance(user, bool) or user is None:
            return {"Message": "Something went wrong"}

        user_id = int(user[1])
        user_scope = user[4]
        picture_bytes = await service.get_google_picture_bytes(user_google_picture_link)

        if picture_bytes is None:
            return {"Message": "Something went wrong"}

        filepath = service.processs_profile_image(user_id, picture_bytes)
        await service.update_profile_image(filepath, user_id)

        token = create_token(username, str(user_id), user_scope)

        return {"access_token": token, "token_type": "bearer", "email": user_email, "username": username, "user_id": user_id, "image_source": filepath}

    else:
        if isinstance(result, bool) or result is None:
            return {"Message": "Later im gonna improve it"}

        existing_user_id = result[1]
        exsisting_image_source = result[2]
        existing_user_scope = result[4]
        token = create_token(username, str(existing_user_id), existing_user_scope)
        return {"access_token": token, "token_type": "bearer", "email": user_email, "username": username, "user_id": existing_user_id, "image_source": exsisting_image_source}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service), verify: Callable = Depends(lambda: verify_password)) -> Dict[str, str]:
    user_name: str = form_data.username

    exist = await service.user_exist_all_data(user_name)

    if not exist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    if isinstance(exist, bool) or exist is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    user_password = exist["hashed_password"]
    if not verify(form_data.password, user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.INVALID_PASSWORD,
        )

    user_scope = exist["role"]
    user_id = str(exist["user_id"])
    user_email = exist["email"]
    image_source = exist["image_source"]
    token = create_token(user_name, user_id, user_scope)

    return {"access_token": token, "token_type": "bearer", "user_email": user_email, "username": user_name, "user_id": user_id, "image_source": image_source}


@app.get("/me", response_model=UserOut)
async def get_my_data(user: str = Depends(get_current_user)):

    return user


@app.patch("/{user_id}/profile/image")
async def update_image(user_id: int, file: UploadFile = File(...), user: str = Security(get_current_user, scopes=["user"]), service: UserService = Depends(get_user_service)) -> Dict[str, str]:

    if isinstance(user, bool) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    if file.size < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MyHttpException.INVALID_IMAGE_SIZE,
        )
    content = await file.read()

    try:
        path = service.processs_profile_image(user_id, content)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MyHttpException.BAD_REQUEST)

    result = await service.update_profile_image(path, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MyHttpException.BAD_REQUEST)

    return {"Message": "Succesfully updated image", "path": path}


@app.post("/product/create")  # TOO LONG ENDPOINT NEED TO REFRACTOR THIS CODE
async def create_product(name: str = Form(...), quantity: int = Form(...), description: str = Form(...), price: float = Form(...), category: str = Form(...), user: str = Security(get_current_user, scopes=["user"]), file: UploadFile = File(...), service: UserService = Depends(get_user_service)):

    try:
        if price < 0 or quantity < 0:
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.INVALID_NUMBER_VALUES,
        )

    content = await file.read()
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.UNAUTHORIZED,
        )

    owner_id = user[4]
    product = service.product_create(name, price, description, quantity, category, int(owner_id))
    await service.send_product_to_data(product)

    product_id_tuple = await service.get_product_id(int(owner_id), name)

    if isinstance(product_id_tuple, bool):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.OTHER_ERROR,
        )

    product_id = product_id_tuple[0]

    filepath = service.processs_main_product_image(product_id, content)

    await service.update_product_image(product_id, filepath)

    return {"Message": "Succesfully added product"}


@app.get("/products")
async def get_all_products(skip: int = 0, service: UserService = Depends(get_user_service)):
    LIMIT = 12
    product_list = await service.get_all_prods(LIMIT, skip)

    return product_list


@app.get("/product/{product_id}", response_model=ProductOut)
async def get_single_product_data(product_id: int, service: UserService = Depends(get_user_service)):
    result = await service.get_single_product(product_id)
    if result is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MyHttpException.NOT_FOUND)
    return result


# @app.get("/{username}/profile")
# async def get_userprofile(user=Security(get_current_user), scopes=["user"]):
#     pass

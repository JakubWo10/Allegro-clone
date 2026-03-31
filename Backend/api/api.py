from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

import jwt
from api.api_models.Google import GoogleToken
from api.api_models.RegUser import Reguser
from api.api_models.UserOut import UserOut
from api.UserService import User_service
from config.config import AVATARS_DIR, PRODUCTS_DIR, settings
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import ExpiredSignatureError
from jwt import PyJWTError
from passlib.context import CryptContext

from .exceptions import MyHttpException

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_passowrd(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_token(username: str, user_id: str) -> str:
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRES)
    payload = {"sub": username, "exp": exp_date, "user_id": user_id}
    return jwt.encode(payload, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)


async def verify_token(token: str) -> Tuple[str, ...] | bool:
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
        username: str = payload.get("sub")
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
        return exist
    except (PyJWTError, ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.INVALID_TOKEN,
        )


@app.post("/register")
async def register(reg_user: Reguser) -> Dict[str, str]:
    user_name = reg_user.name

    exist = await User_service.user_name_exist(user_name)

    if exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=MyHttpException.NAME_IS_TAKEN)

    user_password_hashed = hash_password(reg_user.password)

    user = User_service.create_user(user_password_hashed, reg_user)
    response = await User_service.insert_user(user)

    if response:
        return {"detail": "Poprawnie zarejestrowano użytkownika"}

    return {"detail": "Cos poszło nie tak"}


@app.post("/Google/login")
async def login_google(google_token: GoogleToken):

    try:
        id_info = id_token.verify_oauth2_token(google_token.google_token, requests.Request(), settings.VITE_GOOGLE_CLIENT_ID.get_secret_value())

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidłowy token Google")

    user_email = id_info.get("email")
    user_name = id_info.get("name")
    user_google_id = id_info.get("sub")
    user_google_picture_link = id_info.get("picture")

    result = await User_service.user_name_exist(user_name)

    if not result:

        Google_user = User_service.transform_to_google_user(user_name, user_email, user_google_id)

        await User_service.insert_user(Google_user)
        user = await User_service.user_name_exist(user_name)

        if isinstance(user, bool) or user is None:
            return {"Message": "Cos poszlo nie tak"}

        user_id = int(user[1])
        picture_bytes = await User_service.get_google_picture_bytes(user_google_picture_link)

        if picture_bytes is None:
            return {"Message": "Cos poszlo nie tak"}

        filepath = User_service.processs_profile_image(user_id, picture_bytes)
        await User_service.update_profile_image(filepath, user_id)

        token = create_token(user_name, str(user_id))

        return {"access_token": token, "token_type": "bearer", "email": user_email, "username": user_name, "user_id": user_id}

    else:
        if isinstance(result, bool) or result is None:
            return {"Message": "Potem to usprawnie"}
        existing_user_id = result[1]
        token = create_token(user_name, str(existing_user_id))
        return {"access_token": token, "token_type": "bearer", "email": user_email, "username": user_name, "user_id": existing_user_id}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    user_name: str = form_data.username

    exist = await User_service.user_exist_all_data(user_name)

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

    user_password = exist[1]

    if not verify_passowrd(form_data.password, user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.INVALID_PASSWORD,
        )

    user_id = str(exist[4])
    user_email = exist[3]

    token = create_token(user_name, user_id)
    return {"access_token": token, "token_type": "bearer", "user_email": user_email, "username": user_name}


@app.get("/me", response_model=UserOut)
async def get_my_data(token: str = Depends(oauth2_scheme)):

    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MyHttpException.UNAUTHORIZED)
    print(settings.TOKEN_EXPIRES)
    return user


@app.patch("/{user_id}/profile/image")
async def update_image(user_id: int, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):

    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

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
        path = User_service.processs_profile_image(user_id, content)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MyHttpException.BAD_REQUEST)

    result = await User_service.update_profile_image(path, user_id)
    if not result:
        raise HTTPException(status_code=400, detail=MyHttpException.BAD_REQUEST)

    return {"Message": "Zaktualizowano zdjecie poprawnie"}


@app.post("/product/create")
async def create_product(
    name: str = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(...),
):

    try:
        user = await verify_token(token)
        if not user:
            raise PyJWTError
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    validate_price, validate_quantity = price, quantity
    try:
        if validate_price < 0 or validate_quantity < 1:
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.INVALID_NUMBER_VALUES,
        )

    if isinstance(user, bool) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    owner_id = int(user[4])
    user_from_database = user[0]
    product = User_service.product_create(user_from_database, price, description, quantity, category, owner_id)
    await User_service.send_product_to_data(product)

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.UNAUTHORIZED,
        )

    content = await file.read()
    product_id_tuple = await User_service.get_product_id(int(owner_id), name)

    if isinstance(product_id_tuple, bool):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=MyHttpException.OTHER_ERROR,
        )
    product_id = product_id_tuple[0]

    filepath = User_service.processs_main_product_image(product_id, content)

    await User_service.update_profile_image(filepath, owner_id)

    return {"Message": "Poprawnie dodano produkt"}


@app.get("/products")
async def get_all_products(token: str = Depends(oauth2_scheme)):

    try:
        user = await verify_token(token)
        if not user:
            raise PyJWTError
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

    if isinstance(user, bool) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MyHttpException.UNAUTHORIZED,
        )

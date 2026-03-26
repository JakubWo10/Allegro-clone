from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests
from api.api_models.RegUser import Reguser
from api.api_models.User import User
from api.api_models.GoogleToken import GoogleToken
from typing import Dict, Tuple
import jwt
from datetime import datetime, timedelta, timezone
from jwt import PyJWTError
from api.UserService import User_service
from api.routes.prodcuts import products_router
from api.routes.users import user_router
from config.config import settings, AVATARS_DIR, PRODUCTS_DIR
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import ExpiredSignatureError




app = FastAPI()




app.mount("/avatars", StaticFiles(directory=AVATARS_DIR), name="avatars")
app.mount("/products", StaticFiles(directory=PRODUCTS_DIR), name="products")




app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)




password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_passowrd(password: str, hashed_password: str) -> bool:
        return password_context.verify(password, hashed_password)

def create_token(username: str, user_id: int) -> str:
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRES)
    payload = {
        "sub": username,
        "exp": exp_date,
        "user_id": user_id

    }

    return jwt.encode(payload,settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)


async def verify_token(token: str) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized acces is not legal D:")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidlowy token")
        exist: bool | Tuple[str] = await User_service.user_exist_all_data(username)
        if not exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidlowy token")
        return exist
    except (PyJWTError, ExpiredSignatureError):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidlowy token")




@app.post("/register")
async def register(reg_user: Reguser) -> Dict[str, str]:
    user_name = reg_user.name

    exist: bool | Tuple[str] = await User_service.user_name_exist(user_name)

    if exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Name is already taken")

    user_password_hashed: str = hash_password(reg_user.password)

    user = User_service.create_user(user_password_hashed, reg_user)
    response = await User_service.insert_user(user)

    if response:
        return {"detail": "Poprawnie zarejestrowano użytkownika"}

    return {"detail": "Cos poszło nie tak"}

#musze sie zarejestrowac w chmurze google i potem dokoncze
# @app.post("/Google_login")
# async def login(google_token: GoogleToken):

#     token = google_token.token

#     try:
#         id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

#         user_email = id_info.get("email")
#         user_name = id_info.get('name')
#     except Exception:
#         raise HTTPException(status_code=401, detail="Nieprawidłowy token Google")



@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    user_name: str = form_data.username

    exist: bool | Tuple[str] = await User_service.user_exist_all_data(user_name)

    if not exist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Złe dane logowania")

    user_password: str = exist[1]


    if not verify_passowrd(form_data.password,user_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Złe dane logowania")

    user_id: int =  exist[4]
    image_source: str = exist[2]
    user_email: str = exist[3]

    token: str = create_token(user_name, user_id)
    return {"access_token": token, "token_type": "bearer","user_email": user_email, "image_source": image_source, "user_id": str(user_id) }




@app.get("/me", response_model=User)
async def get_my_data(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NIE MASZ TU DOSTEPU")

    return user




@app.patch("/{user_id}/profile_image")
async def update_image(user_id: int, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):

    user: User = await verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="BRAK AUTORYZACJI")

    if file.size < 0:
        raise HTTPException(status_code=400, detail="Przesłany plik jest pusty")
    content = await file.read()

    try:
        path: str = User_service.processs_profile_image(user_id ,content)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Błąd przetwarzania obrazu:")

    reuslt: str = await User_service.update_profile_image(path, user_id)
    if not reuslt:
        raise HTTPException(status_code=400, detail=f"Wystąpił bląd podczas aktualizowania zdjecia")

    return {"Message": "Zaktualizowano zdjecie poprawnie"}



@app.post("/product/create")
async def create_product (name: str = Form(...), quantity: int = Form(...), description: str = Form(...), price: float = Form(...), category: str = Form(...),
                          token: str = Depends(oauth2_scheme), file: UploadFile = File(...)):

    try:
        user: User = await verify_token(token)
        if not user:
            raise PyJWTError
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nie autoryzowany dostep")



    validate_price, validate_quantity = price, quantity
    try:
        if validate_price < 0 or validate_quantity < 1:
            raise ValueError("Cena lub ilosc produktu nie moze byc ujemna")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="CENA LUB ILOSC PRODUKTU NIE MOZE BYC UJEMNA")

    owner_id: int = user[4]
    name: str = user[0]
    product = User_service.product_create(name, price, description, quantity, category, owner_id)
    await User_service.send_product_to_data(product)

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Tylko zdjecia w formacie png lub jpg")

    content = await file.read()
    product_id_tuple: Tuple[int] = await User_service.get_product_id(owner_id, name)
    product_id: int  = product_id_tuple[0]

    filepath: str = User_service.processs_main_product_image(product_id, content)

    await User_service.update_profile_image(filepath, owner_id)





    return {"Message": "Poprawnie dodano produkt"}



@app.get("/products")
async def get_all_products(token: str = Depends(oauth2_scheme)):

    try:
        user: User = await verify_token(token)
        if not user:
            raise PyJWTError
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nie autoryzowany dostep")


    rows = await User_service.get_all_prods()

    lista = User_service.transform_prods_to_list(rows)

    return lista

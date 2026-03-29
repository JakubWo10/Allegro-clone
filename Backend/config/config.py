import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: SecretStr
    TOKEN_EXPIRES: int

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


current_dir = os.path.dirname(os.path.abspath(__file__))

BACKEND_DIR = os.path.dirname(current_dir)


UPLOAD_DIR = os.path.join(BACKEND_DIR, "uploads")
AVATARS_DIR = os.path.join(UPLOAD_DIR, "avatars")
PRODUCTS_DIR = os.path.join(UPLOAD_DIR, "products")


os.makedirs(AVATARS_DIR, exist_ok=True)
os.makedirs(PRODUCTS_DIR, exist_ok=True)

settings = Settings()

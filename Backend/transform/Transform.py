from api.api_models.RegUser import Reguser
from api.api_models.User import User
from PIL import UnidentifiedImageError, Image, ImageOps
from starlette.concurrency import run_in_threadpool
from fastapi import UploadFile
from PIL import Image, ImageChops, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from io import BytesIO
import os
from config.config import AVATARS_DIR, PRODUCTS_DIR
from api.api_models.Product import Product
from typing import List, Tuple, Dict

class Transform:

    image_url = "test"

    def transform_to_user(self,hashed_password: str, reg_user: Reguser) -> User:
        return User(name=reg_user.name, hashed_password=hashed_password, email=reg_user.email, image_source=self.image_url )

    def create_product(self, name: str, price: float, quantity: int, description: str, category: str, owner_id: int) -> Product:
        return Product(name=name, price=price, description=description, quantity=quantity, main_image=self.image_url, category=category, owner_id=owner_id)

    def process_profile_image(self,user_id: int, file: bytes) -> str:
        with Image.open(BytesIO(file)) as img:

            if img.format.upper() not in ["JPEG", "PNG"]:
                raise UnidentifiedImageError

            img = ImageOps.exif_transpose(img)
            img = ImageOps.fit(img, (600,600), method=Image.Resampling.LANCZOS)

            if img.mode in ["RGBA", "P", "LA"]:
                img = img.convert("RGB")

            filepath: str = f"user_{user_id}.jpg"

            save_path = os.path.join(AVATARS_DIR, filepath)
            img.save(save_path, "JPEG", quality=90)


            return f"/avatars/{filepath}"



    def process_product_main_image(self,product_id: int, file: bytes) -> str:

        with Image.open(BytesIO(file)) as img:


            if img.format.upper() not in ["JPEG", "PNG"]:
                raise UnidentifiedImageError

            img = ImageOps.exif_transpose(img)
            img = ImageOps.fit(img, (300,300), method= Image.Resampling.LANCZOS)

            if img.mode in ["RGBA", "P", "LA"]:
                img = img.convert("RGB")

            filepath = f"produkt_{product_id}.jpg"
            save_path = os.path.join(PRODUCTS_DIR, filepath)
            img.save(save_path, "JPEG", quality =90 )

            return os.path.join("/products/"+filepath)

    def map_to_product_list(self, products: List[Tuple[Product]]) -> List[Product]:

        products_list = []

        for row in products:
            products_list.append({"product_id": row[0],"name": row[1],"price": row[2], "description": row[3], "owner_id": row[4], "category": row[5], "main_image": row[6], "quantity": row[7]})

        return products_list

transformer = Transform()

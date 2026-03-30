from typing import List, Tuple

from api.api_models.Product import Product
from api.api_models.RegUser import Reguser
from api.api_models.User import GoogleUser, User
from database.DataClient import DatabaseClient, data_client
from transform.Transform import Transform, transformer


class UserService:

    def __init__(self, DATA_CLIENT: DatabaseClient, TRANSFORM: Transform) -> None:
        self.data_client = DATA_CLIENT
        self.transform = TRANSFORM

    async def user_exist_all_data(self, username: str) -> Tuple[str, ...] | bool:
        return await self.data_client.user_exist_with_password(username)

    def create_user(self, hashed_password: str, reg_user: Reguser) -> User:
        return self.transform.transform_to_user(hashed_password, reg_user)

    async def insert_user(self, user: User | GoogleUser) -> bool:
        return await self.data_client.insert_user(user)

    def processs_profile_image(self, user_id: int, file: bytes) -> str:
        return self.transform.process_profile_image(user_id, file)

    async def update_profile_image(self, image_source: str, user_id: int) -> bool:
        return await self.data_client.update_image(image_source, user_id)

    async def user_name_exist(self, username: str) -> Tuple[str, ...] | bool:
        return await self.data_client.user_exist(username)

    async def get_google_picture_bytes(self, picture_link: str) -> bytes | None:
        return await self.transform.get_google_user_picture(picture_link)

    # async def user_google_id_exist(self, google_id: str) -> bool:

    #     ...

    def transform_to_google_user(self, name: str, email: str, google_id: str) -> GoogleUser:
        return self.transform.transform_to_google_user(name, email, google_id)

    def product_create(
        self,
        name: str,
        price: float,
        description: str,
        quantity: int,
        category: str,
        owner_id: int,
    ) -> Product:
        return self.transform.create_product(
            name=name,
            price=price,
            description=description,
            quantity=quantity,
            category=category,
            owner_id=str(owner_id),
        )

    async def send_product_to_data(self, product: Product) -> bool:
        return await self.data_client.insert_product(product)

    def processs_main_product_image(self, product_id: int, file: bytes) -> str:
        return self.transform.process_product_main_image(product_id, file)

    async def get_product_id(self, user_id: int, name: str) -> Tuple[int, ...] | bool:
        return await self.data_client.get_user_product(user_id, name)

    async def get_all_prods(self) -> List[Tuple[str, ...]] | bool:
        return await self.data_client.get_all_products()


User_service = UserService(DATA_CLIENT=data_client, TRANSFORM=transformer)

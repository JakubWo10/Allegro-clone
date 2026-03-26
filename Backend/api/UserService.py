from typing import Dict, List, Tuple
from database.DataClient import DatabaseClient
from transform.Transform import Transform
from api.api_models.RegUser import Reguser
from api.api_models.User import User
from database.DataClient import data_client
from transform.Transform import transformer
from api.api_models.Product import Product
import asyncio

class UserService: 

    def __init__(self, DATA_CLIENT: DatabaseClient, TRANSFORM: Transform) -> None:
        self.data_client = DATA_CLIENT
        self.transform = TRANSFORM

    async def user_exist_all_data(self, username: str) -> bool:
        return await self.data_client.user_exist_with_password(username)
    
    def create_user(self,hashed_password: str ,reg_user: Reguser) -> User:
        return self.transform.transform_to_user(hashed_password, reg_user)
    
    async def insert_user(self, user: User) -> bool:
        return await self.data_client.insert_user(user)
    
    def processs_profile_image(self,user_id: int, file: bytes) -> str:
        return self.transform.process_profile_image(user_id, file)
    
    async def update_profile_image(self, image_source: str, user_id: int) -> bool:
        return await self.data_client.update_image(image_source, user_id)
    
    async def user_name_exist(self, username: str) -> bool:
        return await self.data_client.user_exist(username)
    
    def product_create(self, name: str, price: float, description: str, quantity: int, category: str, owner_id: int) -> Product:
        return self.transform.create_product(name=name, price=price, description=description, quantity=quantity, category=category, owner_id=owner_id)

    async def send_product_to_data(self, product: Product) -> bool:
        return await self.data_client.insert_product(product)

    def processs_main_product_image(self, product_id: int, file: bytes) -> str:
        return self.transform.process_product_main_image(product_id, file)

    async def get_product_id(self, user_id: int, name: str ) -> int:
        return await self.data_client.get_user_product(user_id, name)
    
    async def get_all_prods(self) -> Tuple[Product]:
        return await self.data_client.get_all_products()
    
    def transform_prods_to_list(self, rows: Tuple[Product]) -> List[Product]:
        return self.transform.map_to_product_list(rows)
       

User_service = UserService(DATA_CLIENT=data_client, TRANSFORM=transformer) 


from functools import wraps
from typing import Callable, Dict, List, Tuple

from config.config import settings
from database.Contracts import DataProtocol
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def safe_db_call(func: Callable):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except OperationalError:
            return False

    return wrapper


class DatabaseClient:

    _tables: Dict = {
        "Users": {"columns": ("name", "email", "hashed_password", "image_source")},
        "Product": {
            "columns": (
                "name",
                "price",
                "description",
                "owner_id",
                "category",
                "main_image",
                "quantity",
            )
        },
        "Comments": {"columns": ("autor_id", "product_id", "description")},
    }

    def __init__(self, BASE_URL) -> None:
        self.base_url = BASE_URL
        self.engine = create_async_engine(self.base_url, pool_size=10, max_overflow=20)
        self.session_factory = async_sessionmaker(bind=self.engine, class_=AsyncSession)

    def _columns_extractor(self, columns: Tuple[str]) -> str:
        columns_bind: str = ""
        columns_bind = ", ".join(columns)

        return columns_bind

    def _values_extractor(self, values: Dict[str, str]) -> str:
        values_bind_key_list: List[str] = []
        values_bind: str = ""
        for key in values.keys():
            values_bind_key_list.append(f":{key}")

        values_bind = ", ".join(values_bind_key_list)

        return values_bind

    def _insert(self, table_name: str, columns: Tuple[str], values: Dict[str, str]) -> str:
        columns_bind: str = self._columns_extractor(columns)
        values_bind: str = self._values_extractor(values)

        return f"INSERT INTO {table_name} ({columns_bind}) VALUES ({values_bind})"

    def _user_exist(self, table_name: str) -> str:

        return f"SELECT name, user_id, image_source, email FROM {table_name} WHERE name = :name"

    def _user_exist_with_password(self, table_name: str) -> str:

        return f"SELECT name, hashed_password, image_source, email, user_id FROM {table_name} WHERE name = :name"

    def _image_update(self, table_name: str) -> str:

        return f"UPDATE {table_name} SET main_image = :image_source WHERE owner_id = :user_id"

    def _insert_product(self, table_name: str, columns: Tuple[str], values: Dict[str, str]) -> str:
        columns_bind = self._columns_extractor(columns)
        values_bind = self._values_extractor(values)

        return f"INSERT INTO {table_name} ({columns_bind}) VALUES ({values_bind})"

    def _get_user_product(self, table_name: str) -> str:
        return f"SELECT product_id, name, price, description, owner_id, category, main_image, quantity FROM {table_name} WHERE owner_id = :user_id AND name = :name"

    def _get_all_products(self, table_name: str) -> str:

        return f"SELECT product_id, name, price, description, owner_id, category, main_image, quantity FROM {table_name}"

    def _update_product_image(self, table_name: str) -> str:

        return f"UPDATE {table_name} SET main_image = :filepath WHERE product_id = :product_id"

    async def insert_user(self, user_data: DataProtocol) -> bool:
        try:
            async with self.session_factory.begin() as session:
                await session.execute(
                    text(
                        self._insert(
                            "Users",
                            self._tables["Users"]["columns"],
                            user_data.to_dict(),
                        )
                    ),
                    user_data.to_dict(),
                )
                return True
        except OperationalError:
            return False

    async def user_exist_with_password(self, name: str) -> Tuple[str, ...] | bool:
        try:
            async with self.session_factory.begin() as session:  # przy selectach niby nie uzywa sie begin
                result = await session.execute(text(self._user_exist_with_password("Users")), {"name": name})
                row = result.fetchone()

                if row is not None:
                    return row
            return False

        except OperationalError:
            return False

    async def user_exist(self, name: str) -> Tuple[str, ...] | bool:
        try:
            async with self.session_factory.begin() as session:
                result = await session.execute(text(self._user_exist("Users")), {"name": name})
                row = result.fetchone()

                if row is not None:
                    return row
            return False

        except OperationalError:
            return False

    async def update_image(self, image_source: str, user_id: int) -> bool:
        async with self.session_factory.begin() as session:
            try:
                await session.execute(
                    text(self._image_update("Product")),
                    {"image_source": image_source, "user_id": user_id},
                )
                return True

            except OperationalError:
                return False

    async def insert_product(self, data: DataProtocol) -> bool:
        async with self.session_factory.begin() as session:
            try:
                await session.execute(
                    text(
                        self._insert_product(
                            "Product",
                            self._tables["Product"]["columns"],
                            data.to_dict(),
                        )
                    ),
                    data.to_dict(),
                )
                return True
            except OperationalError:
                return False

    async def get_user_product(self, user_id: int, name: str) -> Tuple[int, ...] | bool:

        async with self.session_factory.begin() as session:
            try:
                result = await session.execute(
                    text(self._get_user_product("Product")),
                    {"user_id": user_id, "name": name},
                )
                row = result.fetchone()

                if row is None:
                    return False
                return row
            except OperationalError:
                return False

    async def update_image_product(self, product_id: int, filepath: str) -> bool:

        async with self.session_factory.begin() as session:
            try:
                await session.execute(
                    text(self._update_product_image("Product")),
                    {"product_id": product_id, "filepath": filepath},
                )
                return True

            except OperationalError:
                return False

    # potem zrobie dekorator do try - except
    async def get_all_products(self) -> List[Tuple[str, ...]] | bool:

        async with self.session_factory.begin() as session:
            try:
                all_products = await session.execute(text(self._get_all_products("Product")))
                rows = all_products.fetchall()
                return rows

            except OperationalError:
                return False


data_client = DatabaseClient(settings.DATABASE_URL)

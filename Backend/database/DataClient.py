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
        "Users": {"columns": ("name", "email", "hashed_password", "image_source", "google_id", "role")},
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
        "Comments": {"columns": ("autor_id", "product_id", "description", "created_at")},
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

    def _user_exist(self, table_name: str, column_name: str) -> str:

        return f"SELECT name, user_id, image_source, email, role FROM {table_name} WHERE {column_name} = :{column_name}"

    def _user_exist_with_password(self, table_name: str) -> str:

        return f"SELECT name, hashed_password, image_source, email, user_id, role FROM {table_name} WHERE name = :name"

    def _image_update(self, table_name: str) -> str:

        return f"UPDATE {table_name} SET image_source = :image_source WHERE user_id = :user_id"

    def _get_user_product(self, table_name: str) -> str:
        return f"SELECT product_id, name, price, description, owner_id, category, main_image, quantity FROM {table_name} WHERE owner_id = :user_id AND name = :name"

    def _get_all_products(self, table_name: str) -> str:

        return f"SELECT product_id, name, price, description, owner_id, category, main_image, quantity FROM {table_name} ORDER BY product_id LIMIT :limit OFFSET :offset"

    def _update_product_image(self, table_name: str) -> str:

        return f"UPDATE {table_name} SET main_image = :filepath WHERE product_id = :product_id"

    def _exist_profile_image(self, table_name: str) -> str:

        return f"SELECT user_id FROM {table_name}  WHERE image_source = :path AND user_id = :user_id"

    def _get_prodcut_comment(self, table_name: str) -> str:

        return f"SELECT autor_id, product_id, description, created_at FROM {table_name}"

    def _get_single_product_data(self, table_name: str) -> str:

        return f"SELECT product_id, Product.name, price, description, owner_id, category, main_image, quantity, Users.name, Users.image_source FROM {table_name} JOIN Users ON Users.user_id = Product.owner_id WHERE product_id = :product_id"

    @safe_db_call
    async def insert_user(self, data: DataProtocol) -> bool:
        async with self.session_factory.begin() as session:
            await session.execute(
                text(self._insert("Users", self._tables["Users"]["columns"], data.to_dict())),
                data.to_dict(),
            )
            return True

    @safe_db_call
    async def user_exist_with_password(self, name: str) -> Tuple[str, ...] | bool:
        async with self.session_factory.begin() as session:  # przy selectach niby nie uzywa sie begin
            result = await session.execute(text(self._user_exist_with_password("Users")), {"name": name})
            row = result.fetchone()

            if row:
                return row
        return False

    @safe_db_call
    async def google_id(self, google_id: str) -> bool:
        async with self.session_factory.begin() as session:
            result = await session.execute(text(self._user_exist("Users", "google_id"), {"google_id": google_id}))
            row = result.fetchone()

            if row:
                return True
            return False

    @safe_db_call
    async def user_exist(self, name: str) -> Tuple[str, ...] | bool:
        async with self.session_factory.begin() as session:
            result = await session.execute(text(self._user_exist("Users", "name")), {"name": name})
            row = result.fetchone()

            if row:
                return row
            return False

    @safe_db_call
    async def update_image(self, image_source: str, user_id: int) -> bool:
        async with self.session_factory.begin() as session:
            await session.execute(
                text(self._image_update("Users")),
                {"image_source": image_source, "user_id": user_id},
            )
        return True

    @safe_db_call
    async def insert_product(self, data: DataProtocol) -> bool:
        async with self.session_factory.begin() as session:
            await session.execute(
                text(self._insert("Product", self._tables["Product"]["columns"], data.to_dict())),
                data.to_dict(),
            )
            return True

    @safe_db_call
    async def insert_comment(self, data: DataProtocol) -> bool:
        async with self.session_factory.begin() as session:
            await session.execute(text(self._insert("Comments", self._tables["Comments"]["columns"], data.to_dict())), data.to_dict())

            return True

    @safe_db_call
    async def get_user_product(self, user_id: int, name: str) -> Tuple[int, ...] | bool:
        async with self.session_factory.begin() as session:
            result = await session.execute(
                text(self._get_user_product("Product")),
                {"user_id": user_id, "name": name},
            )
            row = result.fetchone()

            if row:
                return row
            return False

    @safe_db_call
    async def update_image_product(self, product_id: int, filepath: str) -> bool:
        async with self.session_factory.begin() as session:
            await session.execute(
                text(self._update_product_image("Product")),
                {"product_id": product_id, "filepath": filepath},
            )
            return True

    @safe_db_call
    async def get_all_products(self, limit: int, offset: int) -> Dict[str, object] | bool:
        async with self.session_factory.begin() as session:
            all_products = await session.execute(text(self._get_all_products("Product")), {"limit": limit + 1, "offset": offset})
            rows = all_products.fetchall()

            if not rows:
                return False

            if len(rows) > 12:
                has_more = True
            else:
                has_more = False

            return {"products": rows, "has_more": has_more, "skip": offset, "limit": limit}

    @safe_db_call
    async def exist_profile_image(self, user_id: int, path: str) -> bool:
        async with self.session_factory.begin() as session:
            result = await session.execute(text(self._exist_profile_image("Users")), {"user_id": user_id, "path": path})
            row = result.fetchone()

            if row:
                return row
            return False

    @safe_db_call
    async def single_product_data(self, product_id: int) -> Tuple[str, ...] | bool:
        async with self.session_factory.begin() as session:
            result = await session.execute(text(self._get_single_product_data("Product")), {"product_id": product_id})
            row = result.fetchone()
            if row:
                return row
        return False


data_client = DatabaseClient(settings.DATABASE_URL)

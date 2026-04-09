from typing import List, Tuple

from pydantic import BaseModel, Field


class Product(BaseModel):

    product_id: int = Field(description="product_id")
    name: str = Field(min_length=3, max_length=50, description="Name of the product")
    price: float = Field(gt=0, description="Price of product in PLN")
    description: str = Field(min_length=10, max_length=3000, description="detailed product description")
    owner_id: int = Field(description="ID of user who posted the product")
    category: str = Field(description="Category of the posted product")
    main_image: str = Field(description="Main picture of product")
    quantity: int = Field(gt=0, description="Quantinity of product for sale")

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "owner_id": self.owner_id,
            "category": self.category,
            "main_image": self.main_image,
            "quantity": self.quantity,
        }

    @classmethod
    def from_tuples(cls, row: List[Tuple]):
        # product_id, name, price, description, owner_id, category, main_image, quantity FROM {table_name}"
        product = {"product_id": row[0], "name": row[1], "price": row[2], "description": row[3], "owner_id": row[4], "category": row[5], "main_image": row[6], "quantity": row[7]}
        return product

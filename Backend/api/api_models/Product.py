from typing import List, Tuple

from pydantic import BaseModel, Field


class Product(BaseModel):

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
            "main_image": "test",
            "quantity": self.quantity,
        }

    def from_tuples(self, rows: List[Tuple]):
        return Product(name=rows[0])

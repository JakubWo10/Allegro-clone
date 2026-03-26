from typing import Dict, List, Tuple
from pydantic import BaseModel


class Product(BaseModel):

    name: str
    price: float
    description: str
    owner_id: int
    category: str
    main_image: str
    quantity: int

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "owner_id": self.owner_id,
            "category": self.category,
            "main_image": "test",
            "quantity": self.quantity
        }

    def from_tuples(self, rows: List[Tuple]):
        pass

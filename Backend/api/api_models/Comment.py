from datetime import date, datetime

from pydantic import BaseModel


class Comment(BaseModel):

    autor_id: int
    product_id: int
    description: str
    created_at: date

    def to_dict(self):
        return {"autor_id": self.autor_id, "product_id": self.product_id, "description": self.description, "created_at": str(datetime.now().date())}

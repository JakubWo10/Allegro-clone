from typing import Dict

from pydantic import BaseModel, Field


class Reguser(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    email: str
    password: str

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "email": self.email, "password": self.password}

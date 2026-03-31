from typing import Dict

from pydantic import BaseModel, EmailStr, Field


class Reguser(BaseModel):

    name: str = Field(min_length=3, max_length=50, description="Name of the user")
    email: EmailStr = Field(min_length=5, max_length=50, description="Email of user")
    password: str = Field(min_length=3, max_length=200, description="Password before hashing")

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "email": self.email, "password": self.password}

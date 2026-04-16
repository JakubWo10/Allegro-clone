from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    hashed_password: str = Field(min_length=3, max_length=150)
    email: EmailStr = Field(min_length=5, max_length=50)
    google_id: Optional[str] = Field(None)
    image_source: Optional[str] = Field(None)
    role: str = Field(min_length=3, max_length=20)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "email": self.email, "hashed_password": self.hashed_password, "image_source": self.image_source, "google_id": None, "role": self.role}

    @classmethod
    def from_tuple(cls, row: Tuple) -> Dict[str, str]:

        return {"name": row[0], "hashed_password": row[1], "image_source": row[2], "email": row[3], "user_id": row[4], "role": row[5]}


class GoogleUser(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=3, max_length=50)
    google_id: str = Field(min_length=3, max_length=50)
    image_source: Optional[str] = Field(None)
    role: str = Field()

    def to_dict(self) -> Dict:
        return {"name": self.name, "email": self.email, "hashed_password": None, "image_source": self.image_source, "google_id": self.google_id, "role": self.role}


class UserOut(BaseModel):

    name: str = Field(min_length=3, max_length=50, description="Unique name from database")
    email: EmailStr = Field(max_length=150, description="Email from database")
    image_source: str = Field(description="User profile picture")


class Reguser(BaseModel):

    name: str = Field(min_length=3, max_length=50, description="Name of the user")
    email: EmailStr = Field(min_length=5, max_length=50, description="Email of user")
    password: str = Field(min_length=3, max_length=200, description="Password before hashing")

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "email": self.email, "password": self.password}

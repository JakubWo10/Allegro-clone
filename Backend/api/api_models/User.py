from typing import Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    hashed_password: str = Field(min_length=3, max_length=150)
    email: EmailStr = Field(min_length=5, max_length=50)
    google_id: Optional[str] = Field(None)
    image_source: Optional[str] = Field(None)
    role: str = Field(min_length=3, max_length=20)

    def to_dict(self) -> Dict:
        return {"name": self.name, "email": self.email, "hashed_password": self.hashed_password, "image_source": self.image_source, "google_id": None, "role": self.role}


class GoogleUser(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=3, max_length=50)
    google_id: str = Field(min_length=3, max_length=50)
    image_source: Optional[str] = Field(None)
    role: str = Field()

    def to_dict(self) -> Dict:
        return {"name": self.name, "email": self.email, "hashed_password": None, "image_source": self.image_source, "google_id": self.google_id, "role": self.role}

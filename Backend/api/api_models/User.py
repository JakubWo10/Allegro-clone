from pydantic import BaseModel
from typing import Dict, Optional


class User(BaseModel):

    name: str
    hashed_password: str
    email: str
    image_source: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "image_source": self.image_source
        }

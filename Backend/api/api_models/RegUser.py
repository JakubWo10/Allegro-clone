from pydantic import BaseModel, field_validator
from typing import Dict


class Reguser(BaseModel):

    name: str
    email: str
    password: str


    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

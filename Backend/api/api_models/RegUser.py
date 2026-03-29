from typing import Dict

from pydantic import BaseModel


class Reguser(BaseModel):

    name: str
    email: str
    password: str

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "email": self.email, "password": self.password}

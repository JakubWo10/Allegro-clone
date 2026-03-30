from pydantic import BaseModel


class GoogleToken(BaseModel):

    google_token: str

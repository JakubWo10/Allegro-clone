from pydantic import BaseModel, EmailStr, Field


class UserOut(BaseModel):

    name: str = Field(min_length=3, max_length=50, description="Unique name from database")
    email: EmailStr = Field(max_length=150, description="Email from database")
    image_source: str = Field(description="User profile picture")

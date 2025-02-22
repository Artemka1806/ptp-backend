from enum import Enum
from pydantic import BaseModel, EmailStr

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    sex: Sex
    year_of_birth: int
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str

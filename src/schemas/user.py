from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str

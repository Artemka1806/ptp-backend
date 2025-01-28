from datetime import datetime, timedelta

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from pydantic.fields import Field
import jwt

from src.utils import settings


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    name: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.find_one(cls.email == email)

    def dump(self):
        return {**self.model_dump(), "id": str(self.id)}
    
    async def get_plants(self):
        from src.models import Plant
        return await Plant.get_by_owner(self.id)

    def generate_token(self):
        return jwt.encode(
            {"email": self.email, "is_active": self.is_active, "is_superuser": self.is_superuser, "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION)},
            settings.JWT_SECRET,
            algorithm="HS256"
        )
    
    @classmethod
    async def get_by_token(cls, token: str):
        try:
            data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return await cls.find_one(cls.email == data["email"])
    
    class Settings:
        name = "users"

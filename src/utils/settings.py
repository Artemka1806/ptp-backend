from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DB_URI: str
    MONGO_DB_NAME: str
    JWT_SECRET: str
    JWT_EXPIRATION: int = 120
    OPENAI_API_KEY: str
    WEBPUSH_PUBLIC_KEY: str
    WEBPUSH_PRIVATE_KEY: str
    WEBPUSH_EMAIL: str

settings = Settings()

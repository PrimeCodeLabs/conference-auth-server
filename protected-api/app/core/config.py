from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "default_secret"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()

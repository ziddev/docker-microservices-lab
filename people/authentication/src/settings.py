from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_DIRECTORY_PATH: str = "data"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "supersecretkey"


settings = Settings()

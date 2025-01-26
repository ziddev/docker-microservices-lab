from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_DIRECTORY_PATH: str = "data"
    RETRY_LOCK_DELAY: float = 10
    UPDATE_DELAY: float = 10


settings = Settings()

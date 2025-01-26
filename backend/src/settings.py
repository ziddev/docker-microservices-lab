from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_DIRECTORY_PATH: str = "data"
    API_AUTHENTICATION_URL: str = "http://localhost:9021/api/v1/authentications"
    API_USER_URL: str = "http://localhost:9022/api/v1/users"
    API_ARTICLE_URL: str = "http://localhost:9031/api/v1/articles"
    API_PRICE_URL: str = "http://localhost:9032/api/v1/prices"
    API_REVIEW_URL: str = "http://localhost:9033/api/v1/reviews"
    API_STOCK_URL: str = "http://localhost:9041/api/v1/stocks"


settings = Settings()

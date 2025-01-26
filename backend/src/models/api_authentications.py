from pydantic import SecretStr

from http_tool import fetch_data, post_data
from settings import settings


def create_authentication(email: str, password: SecretStr):
    return post_data(f"{settings.API_AUTHENTICATION_URL}",
                     {"email": email, "password": password.get_secret_value()})


def login(email: str, password: str):
    return post_data(f"{settings.API_AUTHENTICATION_URL}/token",
                     {"email": email, "password": password.get_secret_value()})


def me(token: SecretStr):
    return fetch_data(f"{settings.API_AUTHENTICATION_URL}/me",
                      token)

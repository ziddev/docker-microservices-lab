from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import SecretStr

from models.api_authentications import me
from models.api_users import get_user


security = HTTPBearer()


def get_user_info(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    token_info = me(SecretStr(token))
    user = get_user(token_info["sub"])
    return {"token": token_info,
            "user": user}

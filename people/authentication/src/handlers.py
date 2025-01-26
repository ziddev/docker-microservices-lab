from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from settings import settings


from database import (
    get_authentication,
    save_authentication
)
from models import AuthenticationIn


security = HTTPBearer()
router = APIRouter(
    prefix="/api/v1/authentications",
    tags=["Authentications"]
)


def create_access_token(data, expires_delta: timedelta = None) -> str:
    """ Function to create a JWT token """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    """ Decode the JWT token and retrieve the payload information """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.post("",
             status_code=status.HTTP_204_NO_CONTENT)
async def create_authentication(authentication: AuthenticationIn):
    authentication_data = authentication.dict()
    authentication_data["password"] = authentication.password.get_secret_value()
    authentication_email = authentication_data["email"]
    authentication = get_authentication(authentication_email)
    if authentication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication already exists")
    save_authentication(authentication_email, authentication_data)
    return authentication_data


@router.post("/token")
async def login_for_access_token(user_data: AuthenticationIn):
    user = get_authentication(user_data.email)
    if not user or user["password"] != user_data.password.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def decode_my_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    payload = decode_access_token(access_token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

from pydantic import BaseModel, EmailStr, SecretStr


class AuthenticationIn(BaseModel):
    email: EmailStr
    password: SecretStr

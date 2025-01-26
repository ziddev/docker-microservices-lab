from pydantic import BaseModel, EmailStr
from typing import Optional


class UserIn(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    address: str
    phone: str
    comment: Optional[str] = None

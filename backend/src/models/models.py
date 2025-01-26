from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import Optional


class AccountIn(BaseModel):
    email: EmailStr = Field(title="Email", description="The user email", example="firstname.lastname@provider.com")
    password: SecretStr = Field(title="Password", description="The user password", example="password")
    firstname: str = Field(title="Firstname", description="The user firstname", example="Firstname")
    lastname: str = Field(title="Lastname", description="The user lastname", example="Lastname")
    address: str = Field(title="Address", description="The user address", example="11 rue de la Paix, 75000 Paris")
    phone: str = Field(title="Phone", description="The user phone", example="06.15.23.68.22")
    comment: Optional[str] = Field(title="Comment", description="Some comment", default=None, example="It is an account of a user")


class AuthenticateIn(BaseModel):
    email: EmailStr = Field(title="Email", description="The user email", example="firstname.lastname@provider.com")
    password: SecretStr = Field(title="Password", description="The user password", example="password")


class ProductIn(BaseModel):
    title:  str
    description: str
    price: float
    stock: float


class ReviewIn(BaseModel):
    article_id: str
    title:  str
    message: str
    rating: int

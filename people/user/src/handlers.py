from fastapi import APIRouter, HTTPException, status


from database import (
    get_user,
    get_all_users,
    save_user,
    delete_user,
)
from models import UserIn


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.post("")
async def create_user(user: UserIn):
    user_data = user.dict()
    user_email = user_data["email"]
    user = get_user(user_email)
    if user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists")
    user_data["id"] = user_email
    save_user(user_email, user_data)
    return user_data


@router.get("")
async def read_all_users():
    return get_all_users()


@router.get("/{user_email}")
async def read_user(user_email: str):
    user = get_user(user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_email}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_email: str):
    if delete_user(user_email):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

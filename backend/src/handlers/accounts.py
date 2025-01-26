from fastapi import APIRouter, Depends, HTTPException, status

from .common import get_user_info
from models.models import AccountIn, AuthenticateIn
from models.api_authentications import create_authentication, login
from models.api_users import create_user


router = APIRouter(
    prefix="/api/v1/account",
    tags=["Authentications"]
)


@router.post("",
             status_code=status.HTTP_204_NO_CONTENT)
async def create_account(account: AccountIn):
    # Step 1 : Create authentication login(email)/password
    error_apis = []
    try:
        create_authentication(account.email,
                              account.password)
    except Exception as e:
        error_apis.append(e)

    # Step 2 : Create user data
    user = None
    try:
        user = create_user(account.email,
                           account.firstname, account.lastname,
                           account.address, account.phone,
                           account.comment)
    except Exception as e:
        error_apis.append(e)
    if error_apis:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur API(s) externe(s) : {error_apis}")
    return user


@router.post("/_authenticate")
async def authenticate(authenticate: AuthenticateIn):
    token = None
    try:
        token = login(authenticate.email, authenticate.password)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unauthorized")
    return token


@router.get("/me")
async def who_am_i(user_info=Depends(get_user_info)):
    return user_info

from fastapi import APIRouter


from .accounts import router as account_router
from .products import router as products_router


# Include the authentication and product routers which contains routes for interacting with the backend
router: APIRouter = APIRouter(
    prefix="",
    dependencies=[],
    responses={404: {"description": "Not found"}}
)
router.include_router(account_router)
router.include_router(products_router)

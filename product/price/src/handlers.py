from fastapi import APIRouter, HTTPException, status


from database import (
    get_price,
    get_all_prices,
    save_price,
    delete_price,
)
from models import PriceIn


router = APIRouter(
    prefix="/api/v1/prices",
    tags=["Prices"]
)


@router.post("")
async def set_price(price: PriceIn):
    price_data = price.dict()
    article_id = price_data["article_id"]
    price_data = price.dict()
    save_price(article_id, price_data)
    return price_data


@router.get("")
async def read_all_prices():
    return get_all_prices()


@router.get("/{article_id}")
async def read_price(article_id: str):
    price = get_price(article_id)
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return price


@router.delete("/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_price_by_id(article_id: str):
    if delete_price(article_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")

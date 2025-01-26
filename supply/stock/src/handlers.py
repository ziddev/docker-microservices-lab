from fastapi import APIRouter, HTTPException, status
from time import sleep

from database import (
    get_stock,
    get_all_stocks,
    save_stock,
    delete_stock,
    set_lock,
    release_lock
)
from models import StockIn
from settings import settings


router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["Stocks"]
)


def wait_lock(stock_id):
    while True:
        try:
            set_lock(stock_id)
            return
        except Exception:
            sleep(settings.RETRY_LOCK_DELAY)


@router.post("")
async def set_stock(stock: StockIn,
                    fail_if_article_missing: bool = False):
    stock_data = stock.dict()
    article_id = stock_data["article_id"]
    if fail_if_article_missing:
        if not get_stock(article_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    wait_lock(article_id)
    try:
        save_stock(article_id, stock_data)
        return stock_data
    finally:
        release_lock(article_id)


def _change_stock(article_id: str, quantity: float):
    wait_lock(article_id)
    try:
        current_stock = get_stock(article_id)
        if not current_stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        current_stock["stock"] += quantity
        save_stock(article_id, current_stock)
        return current_stock
    finally:
        release_lock(article_id)


@router.post("{article_id}/_increase")
async def increase_stock(article_id: str,
                         quantity: float):
    return _change_stock(article_id, quantity)


@router.post("{article_id}/_decrease")
async def decrease_stock(article_id: str,
                         quantity: float):
    return _change_stock(article_id, -quantity)


@router.get("")
async def read_all_stocks():
    return get_all_stocks()


@router.get("/{article_id}")
async def read_stock(article_id: str):
    stock = get_stock(article_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock


@router.delete("/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_by_id(article_id: str):
    if delete_stock(article_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

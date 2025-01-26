from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from .common import get_user_info
from models.models import ProductIn
from models.api_articles import get_all_articles, create_article, get_article, delete_article
from models.api_prices import get_price, set_price, delete_price
from models.api_reviews import create_review, get_article_reviews, delete_article_reviews
from models.api_stocks import get_stock, set_stock, delete_stock
from settings import settings


router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)


@router.post("")
async def create_product(product: ProductIn,
                         stock_delay: int = 0,
                         user_info = Depends(get_user_info)):
    error_apis = []

    # Step 1 : Create article
    try:
        article = create_article(product.title, product.description)
    except Exception as e:
        error_apis.append(e)

    # Step 2 : Define the price
    article_id = article["id"]
    try:
        price = set_price(article_id, product.price)
    except Exception as e:
        error_apis.append(e)

    # Step 2 : Add a default review
    reviews = None
    try:
        create_review(article_id, f"Article {article_id} added", f"Add at {datetime.now()}", user_info["user"]["email"], None)
        reviews = get_article_reviews(article_id, 1)
    except Exception as e:
        error_apis.append(e)

    # Step 4 : Define the stock
    stock = None
    try:
        stock = set_stock(article_id, product.stock, stock_delay)
    except Exception as e:
        error_apis.append(e)

    if error_apis:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur API(s) externe(s) : {error_apis}")
    return {**article, "reviews": reviews, "price": price["price"], "stock": stock["quantity"]}


def _get_product_extra_infos(article_id, selected_review):
    # Step 1 : Get the price from the Price API
    price = {}
    try:
        price = get_price(article_id)
    except Exception:
        pass

    # Step 2 : Get the reviews from the Review API
    reviews = None
    try:
        reviews = get_article_reviews(article_id, selected_review)
    except Exception:
        pass

    # Step 3 : Get the stock from the Stock API
    stock = {}
    try:
        stock = get_stock(article_id)
    except Exception:
        pass

    # Step 4 : Complete the attributes
    return {"price" : price.get("price", None),
            "reviews" : reviews,
            "stock" : stock.get("quantity", None)}



@router.get("")
async def read_all_products(selected_review: int = 5,
                            _ = Depends(get_user_info)):
    articles = get_all_articles()
    for article in articles:
        article_id = article["id"]
        article_extra = _get_product_extra_infos(article_id, selected_review)
        article.update(article_extra)
    return articles


@router.get("/{article_id}")
async def read_article(article_id: str,
                       selected_review: int = 5,
                       user_info=Depends(get_user_info)):
    article = get_article(article_id)
    article_extra = _get_product_extra_infos(article_id, selected_review)
    article.update(article_extra)
    return article


@router.delete("/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_by_id(article_id: str,
                               user_info=Depends(get_user_info)):
    error_apis = []

    # Step 1 : Delete the stock
    try:
        delete_stock(article_id)
    except Exception as e:
        error_apis.append(e)

    # Step 2 : Delete the reviews
    try:
        delete_article_reviews(article_id)
    except Exception as e:
        error_apis.append(e)

    # Step 3 : Delete the price
    try:
        delete_price(article_id)
    except Exception as e:
        error_apis.append(e)

    # Step 4 : Delete the article
    try:
        delete_article(article_id)
    except Exception as e:
        error_apis.append(e)

    if error_apis:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur API(s) externe(s) : {error_apis}")
from fastapi import APIRouter, HTTPException, status
from uuid import uuid4


from database import (
    get_review,
    get_article_reviews,
    save_review,
    delete_review,
    delete_article_reviews
)
from models import ReviewIn


router = APIRouter(
    prefix="/api/v1/reviews",
    tags=["Reviews"]
)


@router.get("/{review_id}")
async def read_review(review_id: str):
    review = get_review(review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.post("/_search_by_article")
async def search_reviews(article_id: str, selected: int = 10):
    article_review = get_article_reviews(article_id)
    if not article_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article_review[:selected]


@router.post("")
async def add_review(review: ReviewIn,
                     fail_if_article_missing: bool = False):
    review_data = review.dict()
    article_id = review_data["article_id"]
    if fail_if_article_missing:
        if not get_article_reviews(article_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    review_id = str(uuid4())
    review_data["id"] = review_id
    review_data["article_id"] = article_id
    save_review(article_id, review_id, review_data)
    return review_data


@router.delete("/{review_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_by_id(review_id: str):
    if delete_review(review_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")


@router.delete("/_delete_by_article/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_reviews_by_article(article_id: str):
    if delete_article_reviews(article_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

from fastapi import APIRouter, HTTPException, status
from uuid import uuid4


from database import (
    get_article,
    get_all_articles,
    save_article,
    delete_article,
)
from models import ArticleIn


router = APIRouter(
    prefix="/api/v1/articles",
    tags=["Articles"]
)


@router.post("")
async def create_article(article: ArticleIn):
    article_id = str(uuid4())
    article_data = article.dict()
    article_data["id"] = article_id
    save_article(article_id, article_data)
    return article_data


@router.get("")
async def read_all_articles():
    return get_all_articles()


@router.get("/{article_id}")
async def read_article(article_id: str):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article


@router.delete("/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_by_id(article_id: str):
    if delete_article(article_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

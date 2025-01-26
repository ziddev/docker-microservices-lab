from pydantic import BaseModel
from typing import Optional


class ReviewIn(BaseModel):
    article_id: str
    title:  str
    message: str
    user_id: str
    rating: Optional[int]

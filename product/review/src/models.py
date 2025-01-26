from pydantic import BaseModel


class ReviewIn(BaseModel):
    article_id: str
    title:  str
    message: str
    user_id: str

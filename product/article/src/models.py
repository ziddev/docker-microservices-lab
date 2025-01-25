from pydantic import BaseModel


class ArticleIn(BaseModel):
    title:  str
    description: str

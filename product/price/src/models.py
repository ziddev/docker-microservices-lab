from pydantic import BaseModel


class PriceIn(BaseModel):
    article_id:  str
    price: float

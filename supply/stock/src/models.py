from pydantic import BaseModel


class StockIn(BaseModel):
    article_id:  str
    quantity: float

from http_tool import fetch_data, post_data, delete_data
from settings import settings


def get_price(article_id):
    return fetch_data(f"{settings.API_PRICE_URL}/{article_id}")


def set_price(article_id, price):
    return post_data(f"{settings.API_PRICE_URL}?fail_if_article_missing=false",
                     {"article_id": article_id,
                      "price": price})


def delete_price(article_id):
    return delete_data(f"{settings.API_PRICE_URL}/{article_id}")

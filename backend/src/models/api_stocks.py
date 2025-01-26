from http_tool import fetch_data, post_data, delete_data
from settings import settings


def get_stock(article_id):
    return fetch_data(f"{settings.API_STOCK_URL}/{article_id}")


def set_stock(article_id, quantity, stock_delay):
    return post_data(f"{settings.API_STOCK_URL}?fail_if_article_missing=false&update_delay={stock_delay}",
                     {"article_id": article_id, 
                      "quantity": quantity})


def delete_stock(article_id):
    return delete_data(f"{settings.API_STOCK_URL}/{article_id}")


def increase_stock(article_id, quantity, update_delay):
    return post_data(f"{settings.API_STOCK_URL}/{article_id}/_increase?quantity={quantity}&update_delay={update_delay}")


def decrease_stock(article_id, quantity, update_delay):
    return post_data(f"{settings.API_STOCK_URL}/{article_id}/_decrease?quantity={quantity}&update_delay={update_delay}")


def delete_stock(article_id, quantity, update_delay):
    return post_data(f"{settings.API_STOCK_URL}/{article_id}/_increase?update_delay={update_delay}",
                     {"quantity": quantity})

from http_tool import fetch_data, post_data, delete_data
from settings import settings


def get_all_articles():
    return fetch_data(f"{settings.API_ARTICLE_URL}")


def create_article(title, description):
    return post_data(f"{settings.API_ARTICLE_URL}",
                     {"title": title, 
                      "description": description})


def get_article(article_id):
    return fetch_data(f"{settings.API_ARTICLE_URL}/{article_id}")


def delete_article(article_id):
    return delete_data(f"{settings.API_ARTICLE_URL}/{article_id}")

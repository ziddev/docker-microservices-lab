from http_tool import fetch_data, post_data, delete_data
from settings import settings


def get_article_reviews(article_id, selected_review):
    return post_data(f"{settings.API_REVIEW_URL}/_search_by_article?article_id={article_id}&selected={selected_review}")


def create_review(article_id, title, message, user_id, rating):
    return post_data(f"{settings.API_REVIEW_URL}?fail_if_article_missing=false",
                     {"article_id": article_id, 
                      "title": title, 
                      "message": message, 
                      "user_id": user_id, 
                      "rating": rating})


def delete_article_reviews(article_id):
    return delete_data(f"{settings.API_REVIEW_URL}/_delete_by_article/{article_id}")

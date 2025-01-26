import json
from pathlib import Path

from settings import settings


# Directory containing articles JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_article_path(article_id) -> Path:
    """ Returns the path of the file corresponding to a article """
    return Path(DATA_DIRECTORY) / f"{article_id}.json"


def get_all_articles():
    """ Retrieves all articles stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the articles
    articles_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    articles = []
    for article_file in articles_directory.glob("*.json"):
        # For each file, load it and add its content to the list of articles
        with article_file.open("r", encoding="utf-8") as f:
            article_data = json.load(f)
            articles.append(article_data)

    return articles


def get_article(article_id):
    article_file_path = _get_article_path(article_id)

    if not article_file_path.is_file():
        return None
    with article_file_path.open("r", encoding="utf-8") as f:
        article_data = json.load(f)

    return article_data


def save_article(article_id, article_data):
    article_file = _get_article_path(article_id)
    with open(article_file, "w", encoding="utf-8") as f:
        json.dump(article_data, f, indent=4, ensure_ascii=False)


def delete_article(article_id):
    """ Deletes a article by removing its corresponding file """
    article_file_path = _get_article_path(article_id)

    # Check if the file exists
    if article_file_path.is_file():
        # If the file exists, delete it
        article_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False

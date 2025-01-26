import json
from pathlib import Path

from settings import settings


# Directories containing reviews JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
REVIEW_DIRECTORY = Path(DATA_DIRECTORY) / "reviews"
ARTICLE_DIRECTORY = Path(DATA_DIRECTORY) / "articles"

if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
if not ARTICLE_DIRECTORY.exists():
    ARTICLE_DIRECTORY.mkdir(parents=True, exist_ok=True)
if not REVIEW_DIRECTORY.exists():
    REVIEW_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_review_path(review_id) -> Path:
    """ Returns the path of the file corresponding to a review """
    return Path(REVIEW_DIRECTORY) / f"{review_id}.json"


def _get_article_directory(article_id) -> Path:
    """ Returns the path of the directory storing all the article reviews """
    return Path(ARTICLE_DIRECTORY) / f"{article_id}"


def _get_article_review_path(article_id, review_id) -> Path:
    """ Returns the path of the file corresponding to a review according its article """
    return _get_article_directory(article_id) / f"{review_id}.json"


def get_article_reviews(article_id):
    """ Retrieves all reviews of an article stored in JSON files """
    article_reviews_directory = _get_article_directory(article_id)

    if article_reviews_directory.exists():
        reviews = []
        for review_file in article_reviews_directory.glob("*.json"):
            # For each file, load it and add its content to the list of reviews
            with review_file.open("r", encoding="utf-8") as f:
                review_data = json.load(f)
                reviews.append(review_data)
        return reviews
    return None


def get_review(review_id):
    review_file_path = _get_review_path(review_id)

    if not review_file_path.is_file():
        return None
    with review_file_path.open("r", encoding="utf-8") as f:
        review_data = json.load(f)

    return review_data


def save_review(article_id, review_id, review_data):
    # Step 1: Save the review in the general reviews directory
    review_file = _get_review_path(review_id)
    with open(review_file, "w", encoding="utf-8") as f:
        json.dump(review_data, f, indent=4, ensure_ascii=False)

    # Step 2: Save the review in the article reviews directory
    article_review_dir = _get_article_directory(article_id)
    if not article_review_dir.exists():
        article_review_dir.mkdir(parents=True, exist_ok=True)

    article_review_file = _get_article_review_path(article_id, review_id)
    with open(article_review_file, "w", encoding="utf-8") as f:
        json.dump(review_data, f, indent=4, ensure_ascii=False)


def delete_article_reviews(article_id):
    """ Deletes all reviews of an article by removing the directory containing them """
    article_review_dir = _get_article_directory(article_id)
    if article_review_dir.exists():
        for article_review_file in article_review_dir.glob("*.json"):
            # Get the review_id from the article review file
            with article_review_file.open("r", encoding="utf-8") as f:
                review_data = json.load(f)
                review_id = review_data["id"]

            # Delete the article review from the article reviews directory
            article_review_file.unlink()

            # Delete the review from the general reviews directory
            review_file = _get_review_path(review_id)
            review_file.unlink()
        article_review_dir.rmdir()

        return True
    else:
        return False


def delete_review(review_id):
    """ Deletes a review by removing its corresponding file """
    review_file_path = _get_review_path(review_id)
    # Check if the file exists
    if review_file_path.is_file():
        # If the file exists, read the related article_id and delete it
        with review_file_path.open("r", encoding="utf-8") as f:
            review_data = json.load(f)
            article_id = review_data["article_id"]
        review_file_path.unlink()

        # Delete the review from the article reviews directory
        article_review_file_path = _get_article_review_path(article_id, review_id)
        article_review_file_path.unlink()

        # Check if the article reviews directory is empty
        article_review_dir = _get_article_directory(article_id)
        if not any(article_review_dir.iterdir()):
            article_review_dir.rmdir()

        return True
    else:
        # If the file does not exist, return False
        return False

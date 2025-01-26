import json
from pathlib import Path

from settings import settings


# Directory containing prices JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_price_path(price_id) -> Path:
    """ Returns the path of the file corresponding to a price """
    return Path(DATA_DIRECTORY) / f"{price_id}.json"


def get_all_prices():
    """ Retrieves all prices stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the prices
    prices_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    prices = []
    for price_file in prices_directory.glob("*.json"):
        # For each file, load it and add its content to the list of prices
        with price_file.open("r", encoding="utf-8") as f:
            price_data = json.load(f)
            prices.append(price_data)

    return prices


def get_price(price_id):
    price_file_path = _get_price_path(price_id)

    if not price_file_path.is_file():
        return None
    with price_file_path.open("r", encoding="utf-8") as f:
        price_data = json.load(f)

    return price_data


def save_price(price_id, price_data):
    price_file = _get_price_path(price_id)
    with open(price_file, "w", encoding="utf-8") as f:
        json.dump(price_data, f, indent=4, ensure_ascii=False)


def delete_price(price_id):
    """ Deletes a price by removing its corresponding file """
    price_file_path = _get_price_path(price_id)

    # Check if the file exists
    if price_file_path.is_file():
        # If the file exists, delete it
        price_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False

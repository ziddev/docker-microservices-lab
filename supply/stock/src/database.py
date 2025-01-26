import json
from pathlib import Path
from time import sleep

from settings import settings


# Directories containing reviews JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
LOCK_DIRECTORY = Path(DATA_DIRECTORY) / "locks"
STOCK_DIRECTORY = Path(DATA_DIRECTORY) / "stocks"

if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
if not LOCK_DIRECTORY.exists():
    LOCK_DIRECTORY.mkdir(parents=True, exist_ok=True)
if not STOCK_DIRECTORY.exists():
    STOCK_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_lock_path(stock_id) -> Path:
    """ Returns the path of the file corresponding to a stock """
    return Path(LOCK_DIRECTORY) / f"{stock_id}.json"


def _get_stock_path(stock_id) -> Path:
    """ Returns the path of the file corresponding to a stock """
    return Path(STOCK_DIRECTORY) / f"{stock_id}.json"


def get_all_stocks():
    """ Retrieves all stocks stored in JSON files """
    # Path(STOCK_DIRECTORY) points to the directory containing the stocks
    stocks_directory = Path(STOCK_DIRECTORY)

    # We go through all the JSON files in this directory
    stocks = []
    for stock_file in stocks_directory.glob("*.json"):
        # For each file, load it and add its content to the list of stocks
        with stock_file.open("r", encoding="utf-8") as f:
            stock_data = json.load(f)
            stocks.append(stock_data)

    return stocks


def get_stock(stock_id):
    stock_file_path = _get_stock_path(stock_id)

    if not stock_file_path.is_file():
        return None
    with stock_file_path.open("r", encoding="utf-8") as f:
        stock_data = json.load(f)

    return stock_data


def save_stock(stock_id, stock_data):
    stock_file = _get_stock_path(stock_id)
    sleep(10)
    with open(stock_file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4, ensure_ascii=False)
    # Add a function to set a lock on the stock


def delete_stock(stock_id):
    """ Deletes a stock by removing its corresponding file """
    stock_file_path = _get_stock_path(stock_id)

    # Check if the file exists
    if stock_file_path.is_file():
        # If the file exists, delete it
        stock_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False


def set_lock(stock_id):
    lock_file = _get_lock_path(stock_id)
    lock_data = {"stock_id": stock_id}
    with open(lock_file, "a", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=4, ensure_ascii=False)


def release_lock(stock_id):
    lock_file = _get_lock_path(stock_id)
    if lock_file.is_file():
        lock_file.unlink()

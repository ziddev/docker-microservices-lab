import json
from pathlib import Path

from settings import settings


# Directory containing users JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_user_path(user_id) -> Path:
    """ Returns the path of the file corresponding to a user """
    return Path(DATA_DIRECTORY) / f"{user_id}.json"


def get_all_users():
    """ Retrieves all users stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the users
    users_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    users = []
    for user_file in users_directory.glob("*.json"):
        # For each file, load it and add its content to the list of users
        with user_file.open("r", encoding="utf-8") as f:
            user_data = json.load(f)
            users.append(user_data)

    return users


def get_user(user_id):
    user_file_path = _get_user_path(user_id)

    if not user_file_path.is_file():
        return None
    with user_file_path.open("r", encoding="utf-8") as f:
        user_data = json.load(f)

    return user_data


def save_user(user_id, user_data):
    user_file = _get_user_path(user_id)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)


def delete_user(user_id):
    """ Deletes a user by removing its corresponding file """
    user_file_path = _get_user_path(user_id)

    # Check if the file exists
    if user_file_path.is_file():
        # If the file exists, delete it
        user_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False

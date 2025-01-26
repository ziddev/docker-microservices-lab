import json
from pathlib import Path

from settings import settings


# Directory containing authentications JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY_PATH)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_authentication_path(authentication_id) -> Path:
    """ Returns the path of the file corresponding to a authentication """
    return Path(DATA_DIRECTORY) / f"{authentication_id}.json"


def get_authentication(authentication_id):
    authentication_file_path = _get_authentication_path(authentication_id)

    if not authentication_file_path.is_file():
        return None
    with authentication_file_path.open("r", encoding="utf-8") as f:
        authentication_data = json.load(f)

    return authentication_data


def save_authentication(authentication_id, authentication_data):
    authentication_file = _get_authentication_path(authentication_id)
    with open(authentication_file, "w", encoding="utf-8") as f:
        json.dump(authentication_data, f, indent=4, ensure_ascii=False)

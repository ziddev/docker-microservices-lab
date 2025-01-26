from enum import Enum
from fastapi import HTTPException, status
from pydantic import SecretStr
import requests


default_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


def _request(method, url, body={}, token: SecretStr = None):
    try:
        headers = default_headers
        if token:
            headers["Authorization"] = f"Bearer {token.get_secret_value()}"

        res = None
        if method == HttpMethod.GET:
            res = requests.get(url, headers=headers)
        elif method == HttpMethod.POST:
            res = requests.post(url, json=body, headers=headers)
        elif method == HttpMethod.DELETE:
            res = requests.delete(url, headers=headers)

        if res.status_code < status.HTTP_200_OK or res.status_code >= status.HTTP_400_BAD_REQUEST:
            raise HTTPException(status_code=res.status_code, detail=res.json())
        if res.status_code == status.HTTP_204_NO_CONTENT:
            return None
        return res.json()
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur API externe : {url}")


def fetch_data(url, token: SecretStr = None):
    return _request(HttpMethod.GET, url, None, token)


def post_data(url, body={}, token: SecretStr = None):
    return _request(HttpMethod.POST, url, body, token)


def delete_data(url, token: SecretStr = None):
    return _request(HttpMethod.DELETE, url, None, token)

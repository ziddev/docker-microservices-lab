from http_tool import fetch_data, post_data
from settings import settings


def create_user(email,
                firstname, lastname,
                address, phone,
                comment):
    return post_data(f"{settings.API_USER_URL}",
                     {"email": email, 
                      "firstname": firstname, "lastname": lastname, 
                      "address": address, "phone": phone,
                      "comment": comment})

def get_user(user_email):
    return fetch_data(f"{settings.API_USER_URL}/{user_email}")

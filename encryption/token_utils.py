import jwt
from jwt import InvalidSignatureError
from settings import token_key
from typing import Union


def generate_token(license_id: int) -> str:
    token = jwt.encode({"license_id": license_id}, token_key, algorithm="HS256")

    return token


def verify_token(token) -> Union[dict, bool]:
    try:
        decoded_jwt = jwt.decode(token, token_key, algorithms=["HS256"])
    except InvalidSignatureError:
        decoded_jwt = False

    return decoded_jwt

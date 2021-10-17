from jwt import InvalidSignatureError, encode, decode
from settings import token_key
from typing import Optional


def generate_token(license_id: int) -> str:
    token = encode({"license_id": license_id}, token_key, algorithm="HS256")

    return token


def validate_token(token: str) -> Optional[dict]:
    try:
        decoded_jwt = decode(token, token_key, algorithms=["HS256"])
    except InvalidSignatureError:
        decoded_jwt = None

    return decoded_jwt

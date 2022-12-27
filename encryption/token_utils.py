import jwt

import settings


def generate_token(license_id: int) -> str:
    token = jwt.encode({"license_id": license_id}, settings.token_key,
                       algorithm="HS256")

    return token


def validate_token(token: str):
    try:
        decoded_jwt = jwt.decode(token, settings.token_key,
                                 algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        decoded_jwt = None

    return decoded_jwt

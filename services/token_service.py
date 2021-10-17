from datetime import datetime
from db_models.license import License
from encryption.token_utils import validate_token


def verify_token(received_token: str) -> bool:
    decoded_token = validate_token(received_token)

    if decoded_token:
        stored_license = License.query.get(decoded_token["license_id"])

        if stored_license and stored_license.expiration_date >= datetime.today().date():
            return True

    return False

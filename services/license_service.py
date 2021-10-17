from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Optional
from db_models.shared import db
from db_models.license import License
from encryption.token_utils import generate_token


def create_license(expiration_days: int) -> str:
    new_license = token_urlsafe(16)
    expiration_date = datetime.today() + timedelta(days=expiration_days)

    license_obj = License(value=new_license, expiration_date=expiration_date)

    db.session.add(license_obj)
    db.session.commit()

    return license_obj.value


def extend_license(received_license: str, expiration_days: int) -> bool:
    stored_license = License.query.filter_by(value=received_license).first()

    if stored_license:
        current_date = datetime.today().date()

        if stored_license.expiration_date > current_date:
            stored_license.expiration_date += timedelta(days=expiration_days)
        else:
            stored_license.expiration_date = current_date + timedelta(days=expiration_days)

        db.session.commit()

        return True

    return False


def verify_license(received_license: str) -> Optional[str]:
    stored_license = License.query.filter_by(value=received_license).first()
    current_date = datetime.today().date()

    if stored_license and not stored_license.has_been_used and stored_license.expiration_date >= current_date:
        token = generate_token(stored_license.id)
        stored_license.token = token
        stored_license.has_been_used = True

        db.session.commit()

        return token

from datetime import datetime, timedelta
from secrets import token_urlsafe
from http import HTTPStatus
from flask import Blueprint, Response, request
from db_models.shared import db
from db_models.license import License
from encryption.token_utils import generate_token, verify_token
from settings import master_key, client_key

license_controller = Blueprint("license_controller", __name__)


@license_controller.route("/createlicense")
def create_license() -> Response:
    auth_key = request.headers.get("auth")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and expiration_days:
        new_license = token_urlsafe(16)
        expiration_date = datetime.today() + timedelta(days=float(expiration_days))

        license_obj = License(value=new_license, expiration_date=expiration_date)

        db.session.add(license_obj)
        db.session.commit()

        return Response(response=new_license, status=HTTPStatus.CREATED, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/extendlicense", methods=['POST'])
def extend_license() -> Response:
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and received_license and expiration_days:
        stored_license = License.query.filter_by(value=received_license).first()

        if stored_license:
            current_date = datetime.today().date()

            if stored_license.expiration_date > current_date:
                stored_license.expiration_date += timedelta(days=float(expiration_days))
            else:
                stored_license.expiration_date = current_date + timedelta(days=float(expiration_days))

            db.session.commit()

            return Response(response="License has been extended", status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/verifylicense", methods=['POST'])
def verify_license() -> Response:
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")

    if auth_key == client_key and received_license:
        stored_license = License.query.filter_by(value=received_license).first()

        if stored_license and not stored_license.has_been_used:
            token = generate_token(stored_license.id)
            stored_license.token = token
            stored_license.has_been_used = True

            db.session.commit()

            return Response(response=token, status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/authenticatetoken", methods=['POST'])
def authenticate_token() -> Response:
    auth_key = request.headers.get("auth")
    received_token = request.form.get("token")

    if auth_key == client_key and received_token:
        decoded_token = verify_token(received_token)

        if decoded_token:
            stored_license = License.query.get(decoded_token["license_id"])

            if stored_license and stored_license.expiration_date >= datetime.today().date():
                return Response(response="Valid token", status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")

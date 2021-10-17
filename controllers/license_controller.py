from http import HTTPStatus
from flask import Blueprint, Response, request
from settings import master_key, client_key
from services import license_service, token_service

license_controller = Blueprint("license_controller", __name__)


@license_controller.route("/createlicense")
def create_license() -> Response:
    auth_key = request.headers.get("auth")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and expiration_days.isdecimal():
        created_license = license_service.create_license(int(expiration_days))

        return Response(response=created_license, status=HTTPStatus.CREATED, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/extendlicense", methods=['POST'])
def extend_license() -> Response:
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and received_license and expiration_days.isdecimal():
        if license_service.extend_license(received_license, int(expiration_days)):
            return Response(response="License has been extended", status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/verifylicense", methods=['POST'])
def verify_license() -> Response:
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")

    if auth_key == client_key and received_license:
        token = license_service.verify_license(received_license)

        if token:
            return Response(response=token, status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")


@license_controller.route("/authenticatetoken", methods=['POST'])
def authenticate_token() -> Response:
    auth_key = request.headers.get("auth")
    received_token = request.form.get("token")

    if auth_key == client_key and received_token:
        if token_service.verify_token(received_token):
            return Response(response="Valid token", status=HTTPStatus.OK, mimetype="text/plain")

    return Response(response="Invalid request", status=HTTPStatus.FORBIDDEN, mimetype="text/plain")

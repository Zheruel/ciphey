from http import HTTPStatus

from flask import Blueprint, Response, request

from services import license_service, token_service
from settings import master_key, client_key
from static_values import license_urls, generic_response

license_controller = Blueprint("license_controller", __name__)


@license_controller.route(license_urls.CREATE_LICENSE)
def create_license():
    auth_key = request.headers.get("auth")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and expiration_days.isdecimal():
        created_license = license_service.create_license(int(expiration_days))

        return Response(response=created_license, status=HTTPStatus.CREATED)

    return Response(response=generic_response.INVALID_REQUEST,
                    status=HTTPStatus.FORBIDDEN)


@license_controller.route(license_urls.EXTEND_LICENSE, methods=['POST'])
def extend_license():
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")
    expiration_days = request.form.get("expiration_days")

    if auth_key == master_key and received_license and expiration_days.isdecimal():
        if license_service.extend_license(received_license,
                                          int(expiration_days)):
            return Response(response="License has been extended",
                            status=HTTPStatus.OK)

    return Response(response=generic_response.INVALID_REQUEST,
                    status=HTTPStatus.FORBIDDEN)


@license_controller.route(license_urls.VERIFY_LICENSE, methods=['POST'])
def verify_license():
    auth_key = request.headers.get("auth")
    received_license = request.form.get("license")

    if auth_key == client_key and received_license:
        token = license_service.verify_license(received_license)

        if token:
            return Response(response=token, status=HTTPStatus.OK,
                            )

    return Response(response=generic_response.INVALID_REQUEST,
                    status=HTTPStatus.FORBIDDEN)


@license_controller.route(license_urls.AUTHENTICATE_TOKEN, methods=['POST'])
def authenticate_token():
    auth_key = request.headers.get("auth")
    received_token = request.form.get("token")

    if auth_key == client_key and received_token:
        if token_service.verify_token(received_token):
            return Response(response="Valid token", status=HTTPStatus.OK)

    return Response(response=generic_response.INVALID_REQUEST,
                    status=HTTPStatus.FORBIDDEN)

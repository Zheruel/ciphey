import pytest
from http import HTTPStatus
from main import app, db
from settings import master_key, client_key
from db_models.license import License
from datetime import datetime, timedelta


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client


def test_create_license(client):
    # Expiration days and auth key not correct
    rv = client.get("/createlicense")

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # Auth key and expiration days correct
    rv = client.get("/createlicense", data={"expiration_days": "30"}, headers={"auth": master_key})

    assert rv.status_code == HTTPStatus.CREATED


def test_extend_license(client):
    # Expiration days license and auth key not correct
    rv = client.post("/extendlicense")

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # License does not exist
    rv = client.post("/extendlicense", data={"expiration_days": "30", "license": "123"}, headers={"auth": master_key})

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # License exists and expiration date > current date
    expiration_date = datetime.today() + timedelta(days=30)

    db.session.add(License(value="123", expiration_date=expiration_date))
    db.session.commit()

    client.post("/extendlicense", data={"expiration_days": "30", "license": "123"}, headers={"auth": master_key})

    extended_license = License.query.filter_by(value="123").first()
    extended_date = expiration_date + timedelta(days=30)

    assert extended_license.expiration_date == extended_date.date()

    # License exists and expiration date <= current date
    expired_date = datetime.today() - timedelta(days=30)

    db.session.add(License(value="231", expiration_date=expired_date))
    db.session.commit()

    client.post("/extendlicense", data={"expiration_days": "30", "license": "231"}, headers={"auth": master_key})

    extended_license = License.query.filter_by(value="231").first()

    assert extended_license.expiration_date == expiration_date.date()


def test_verify_license(client):
    # License and auth key not correct
    rv = client.post("/verifylicense")

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # License does not exist or it has been used before
    db.session.add(License(value="used", expiration_date=datetime.today(), has_been_used=True))
    db.session.commit()

    rv = client.post("/verifylicense", data={"license": "123"}, headers={"auth": client_key})

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # License and token are valid
    db.session.add(License(value="123", expiration_date=datetime.today()))
    db.session.commit()

    rv = client.post("/verifylicense", data={"license": "123"}, headers={"auth": client_key})

    assert rv.status_code == HTTPStatus.OK

    # Valid license now has token
    license_obj = License.query.filter_by(value="123").first()

    assert license_obj.token


def test_authenticate_token(client):
    # Auth key and token not correct
    rv = client.post("/authenticatetoken")

    assert rv.status_code == HTTPStatus.FORBIDDEN

    # Valid token and auth key
    db.session.add(License(value="123", expiration_date=datetime.today()))
    db.session.commit()

    rv = client.post("/verifylicense", data={"license": "123"}, headers={"auth": client_key})
    token = rv.data.decode("utf-8")

    rv = client.post("/authenticatetoken", data={"token": token}, headers={"auth": client_key})
    assert rv.status_code == HTTPStatus.OK

    # Token attached to expired license
    expired_date = datetime.today() - timedelta(days=30)

    license_obj = License.query.filter_by(value="123").first()
    license_obj.expiration_date = expired_date

    db.session.commit()

    rv = client.post("/authenticatetoken", data={"token": token}, headers={"auth": client_key})
    assert rv.status_code == HTTPStatus.FORBIDDEN


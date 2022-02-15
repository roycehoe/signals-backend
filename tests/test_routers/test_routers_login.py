from pytest_freezegun import freeze_time

from app import config
from tests.fixtures.config import client


@freeze_time("2021-04-20")
def test_login_valid_credentials(mock_user, token_expiry):
    """Ensures users will receive JWT token upon submitting valid credentials"""
    response = client.post(
        "/login",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjIwNjA0ODYwfQ.3LzkSgYNLT2xQhQu27FL4SoLjE5qg4x7StlAn9u27f0",
        "token_type": "bearer",
    }
    pass


def test_login_invalid_credentials(mock_no_user):
    """Ensures users will receive custom error upon authentication failure"""

    response = client.post(
        "/login",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "INVALID_CREDENTIALS"}}


def test_login_no_username(mock_user):
    """Ensures users must log in with a username"""

    response = client.post(
        "/login",
        json={
            "password": "bravo",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        }
    }


def test_login_no_password(mock_user):
    """Ensures users must log in with a password"""

    response = client.post(
        "/login",
        json={
            "username": "alpha",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        }
    }


def test_login_no_username_no_password(mock_user):
    """Ensures users cannot login without providing both username and password"""

    response = client.post(
        "/login",
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        }
    }


def test_login_malformed_request():
    """Ensures a malformed request raises a custom error"""

    response = client.post("/user/new", data='{"1"}')
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MALFORMED_REQUEST_ERROR",
            "msg": [
                {
                    "ctx": {
                        "colno": 5,
                        "doc": '{"1"}',
                        "lineno": 1,
                        "msg": "Expecting ':' delimiter",
                        "pos": 4,
                    },
                    "loc": ["body", 4],
                    "msg": "Expecting ':' delimiter: line 1 column 5 (char 4)",
                    "type": "value_error.jsondecode",
                }
            ],
        },
    }

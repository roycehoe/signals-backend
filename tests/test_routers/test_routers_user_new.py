from tests.fixtures.config import client


def test_create_user(user_creation_success):
    """Ensures that new users can be created"""

    response = client.post(
        "/user/new",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"username": "alpha"}


def test_create_users_same_username(user_creation_failure):
    """Ensures that new users must have unique usernames"""

    response = client.post(
        "/user/new",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "USERNAME_TAKEN"}}


def test_create_users_same_password(user_creation_success):
    """Ensures that new users can have similar passwords"""

    response = client.post(
        "/user/new",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )

    response = client.post(
        "/user/new",
        json={
            "username": "charlie",
            "password": "bravo",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"username": "charlie"}


def test_create_users_same_username_same_password(user_creation_failure):
    """Ensures that new users must have unique usernames even if the same passowrd exists in the database"""

    response = client.post(
        "/user/new",
        json={
            "username": "alpha",
            "password": "bravo",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "USERNAME_TAKEN"}}


def test_create_users_no_username():
    """Ensures that new users must provide a username"""

    response = client.post(
        "/user/new",
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


def test_create_users_no_password():
    """Ensures that new users must provide a password"""

    response = client.post(
        "/user/new",
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


def test_create_users_no_username_no_password():
    """Ensures that new users cannot leave username and password empty"""

    response = client.post("/user/new", json={})
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


def test_create_users_malformed_request():
    """Ensures a malformed request raises a custom error"""

    response = client.post("/user/new", data="{'1'}")
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MALFORMED_REQUEST_ERROR",
            "msg": [
                {
                    "ctx": {
                        "colno": 2,
                        "doc": "{'1'}",
                        "lineno": 1,
                        "msg": "Expecting property name enclosed in double quotes",
                        "pos": 1,
                    },
                    "loc": ["body", 1],
                    "msg": "Expecting property name enclosed in double "
                    "quotes: line 1 column 2 (char 1)",
                    "type": "value_error.jsondecode",
                }
            ],
        }
    }

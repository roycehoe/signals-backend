from pytest_freezegun import freeze_time

from tests.fixtures.config import client


def test_game_play_no_token():
    """Ensures that authentication fails if users provide no authentication token"""

    response = client.post("/game/play", json={"prediction": "Higher", "bet": 1})
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "MISSING_AUTHENTICATION_TOKEN"}}


def test_game_play_invalid_token():
    """Ensures that authentication fails if users provide an invalid token"""

    response = client.post(
        "/game/play",
        headers={"token": "an_invalid_token"},
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


def test_game_game_invalid_JWT_token():
    """Ensures that authentication fails if users provide an invalid JWT token"""

    response = client.post(
        "/game/play",
        headers={"token": "an_invalid_token"},
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


def test_game_game_malformed_request():
    """Ensures custom error raised if request is malformed"""

    response = client.post(
        "/game/play", headers={"token": "an_invalid_token"}, data="malformed"
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MALFORMED_REQUEST_ERROR",
            "msg": [
                {
                    "ctx": {
                        "colno": 1,
                        "doc": "malformed",
                        "lineno": 1,
                        "msg": "Expecting value",
                        "pos": 0,
                    },
                    "loc": ["body", 0],
                    "msg": "Expecting value: line 1 column 1 (char 0)",
                    "type": "value_error.jsondecode",
                }
            ],
        }
    }


def test_game_game_missing_prediction(valid_token):
    """Ensures that custom error is raised if users do not include Prediction in their request"""

    response = client.post(
        "/game/play",
        headers={"token": "an_invalid_token"},
        json={"bet": 1},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body", "prediction"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        }
    }


@freeze_time("2021-04-20")
def test_game_game_missing_bet(valid_token):
    """Ensures that custom error is raised if users do not include bet in their request"""

    response = client.post(
        "/game/play",
        headers={"token": "an_invalid_token"},
        json={"bet": 1},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body", "prediction"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        }
    }


@freeze_time("2021-04-20")
def test_game_game_missing_prediction_and_bet():
    """Ensures that custom error is raised if users do not include bet and prediction in their request"""

    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "MISSING_FIELD_VALUES",
            "msg": [
                {
                    "loc": ["body"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        }
    }


@freeze_time("2021-04-20")
def test_game_game_new_user(no_gamestate, mock_user):
    """Ensures users attempting to play without an existing gamestate will raise a custom error"""

    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "GAME_NOT_CREATED"}}


@freeze_time("2021-04-20")
def test_game_game_round_ended(
    end_gamestate,
):
    """Ensures custom error raised if users attempt to play when round has ended"""

    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"error": "ROUND_NOT_STARTED"}}


@freeze_time("2021-04-20")
def test_game_game_end_round_prediction_higher_win(
    start_gamestate_next_card_higher,
    mock_user,
):
    """Ensures expected result if players win when their prediction is higher"""

    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1001,
        "next_card": {"name": "Ace of Hearts", "rank": "A", "suit": "H"},
        "player_name": "alpha",
        "round": 1,
        "win": True,
    }


@freeze_time("2021-04-20")
def test_game_game_end_round_prediction_lower_lose(
    start_gamestate_next_card_higher,
    mock_user,
):
    """Ensures expected result if players lose when their prediction is lower"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Lower", "bet": 1},
    )
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 999,
        "next_card": {"name": "Ace of Hearts", "rank": "A", "suit": "H"},
        "player_name": "alpha",
        "round": 1,
        "win": False,
    }


@freeze_time("2021-04-20")
def test_game_game_end_round_prediction_lower_win(
    start_gamestate_next_card_lower,
    mock_user,
):
    """Ensures expected result if players win when their prediction is lower and the next card is lower"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Lower", "bet": 1},
    )
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1001,
        "next_card": {"name": "Two of Hearts", "rank": "2", "suit": "H"},
        "player_name": "alpha",
        "round": 1,
        "win": True,
    }


@freeze_time("2021-04-20")
def test_game_game_end_round_prediction_higher_lose(
    start_gamestate_next_card_lower,
    mock_user,
):
    """Ensures expected result if players lose when their prediction is higher and the next card is lower"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 1},
    )
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 999,
        "next_card": {"name": "Two of Hearts", "rank": "2", "suit": "H"},
        "player_name": "alpha",
        "round": 1,
        "win": False,
    }


@freeze_time("2021-04-20")
def test_game_game_bet_exceeds_money(
    start_gamestate_next_card_lower,
    mock_user,
):
    """Ensures custom error is raised if player bet exceeds money"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 1001},
    )
    assert response.json() == {"detail": {"error": "INVALID_BET"}}


@freeze_time("2021-04-20")
def test_game_game_bet_is_zero(
    start_gamestate_next_card_lower,
    mock_user,
):
    """Ensures custom error is raised if player bet is zero"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": 0},
    )
    assert response.json() == {"detail": {"error": "INVALID_BET"}}


def test_game_game_bet_is_negative(
    start_gamestate_next_card_lower,
    mock_user,
):
    """Ensures custom error is raised if player bet is zero"""
    response = client.post(
        "/game/play",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
        json={"prediction": "Higher", "bet": -1},
    )
    assert response.json() == {"detail": {"error": "INVALID_BET"}}

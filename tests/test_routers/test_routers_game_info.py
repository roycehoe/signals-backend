from pytest_freezegun import freeze_time

from hilo.models.gamestate import GameState
from tests.fixtures.config import client


def test_game_info_no_token():
    """Ensures that authentication fails if users provide no authentication token"""

    response = client.get(
        "/game/info",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "MISSING_AUTHENTICATION_TOKEN"}}


def test_game_info_invalid_token():
    """Ensures that authentication fails if users provide an invalid token"""

    response = client.get(
        "/game/info",
        headers={"token": "an_invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


def test_game_info_invalid_JWT_token():
    """Ensures that authentication fails if users provide an invalid JWT token"""

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


@freeze_time("2021-04-20")
def test_game_info_reflects_changed_gamestate(
    monkeypatch,
    start_gamestate_next_card_higher,
):
    """Ensures that game info reflects changing gamestates"""

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }

    def create_mock_gamestate(*args, **kwargs):
        return GameState("beta", shuffle_deck=True)

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_mock_gamestate,
    )

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "base_card": None,
        "money": 1000,
        "player_name": "beta",
        "round": 1,
    }


@freeze_time("2021-04-20")
def test_game_info_round_not_started(no_gamestate):
    """Ensures custom error is raised if game info is requested when no game has been started"""

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "GAME_NOT_CREATED"}}


@freeze_time("2021-04-20")
def test_game_info_round_started(start_gamestate_next_card_higher):
    """Ensures expected response if hilo round has started"""

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }


@freeze_time("2021-04-20")
def test_game_info_provides_consistent_response(
    start_gamestate_next_card_higher,
):
    """Ensures consistent response if game info request is successful"""

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }

    response = client.get(
        "/game/info",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "base_card": {"name": "Seven of Diamonds", "rank": "7", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }

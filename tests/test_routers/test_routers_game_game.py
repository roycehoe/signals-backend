import pytest
from pytest_freezegun import freeze_time

from hilo.models.deck import Deck
from hilo.models.gamestate import GameState
from tests.fixtures.config import client


def test_game_game_no_token():
    """Ensures that authentication fails if users provide no authentication token"""

    response = client.get(
        "/game/game",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "MISSING_AUTHENTICATION_TOKEN"}}


def test_game_game_invalid_token():
    """Ensures that authentication fails if users provide an invalid token"""

    response = client.get(
        "/game/game",
        headers={"token": "an_invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


def test_game_game_invalid_JWT_token():
    """Ensures that authentication fails if users provide an invalid JWT token"""

    response = client.get(
        "/game/game",
        headers={"token": "an_invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": {"error": "TOKEN_AUTHENTICATION_FAILED"}}


@freeze_time("2021-04-20")
def test_game_game_new_round(end_gamestate, mock_user):
    """Ensures new round is started for an existing player"""

    response = client.get(
        "/game/game",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "base_card": {"name": "Two of Diamonds", "rank": "2", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 2,
    }


@freeze_time("2021-04-20")
def test_game_game_new_game(
    mock_user,
    unshuffled_deck,
    no_gamestate,
    save_new_gamestate,
    update_new_gamestate,
):
    """Ensures new game is started for an existing player"""

    response = client.get(
        "/game/game",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "base_card": {"name": "Two of Diamonds", "rank": "2", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }


@freeze_time("2021-04-20")
def test_game_game_when_round_not_ended(start_gamestate_next_card_higher):
    """Ensures that a custom error is raised if players start a round without ending a round"""

    response = client.get(
        "/game/game",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E",
        },
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"error": "ROUND_NOT_ENDED"}}


@freeze_time("2021-04-20")
def test_game_game_when_bankrupt(
    bankrupt_gamestate,
    mock_user,
    unshuffled_deck,
    update_new_gamestate,
):
    """Ensures new round is started for a bankrupt player"""

    response = client.get(
        "/game/game",
        headers={
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFscGhhIiwiZXhwIjoxNjE5MDQ5NjAwfQ.KpRkjrjrEcfkrAw_lf8tRXayIcSqc125cMNmm-Dui5E"
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "base_card": {"name": "Two of Diamonds", "rank": "2", "suit": "D"},
        "money": 1000,
        "player_name": "alpha",
        "round": 1,
    }

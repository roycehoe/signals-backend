import pytest

from app.errors import GameStateStoreNotFoundError
from app.models import GameStateStore
from hilo.models.gamestate import Card, Deck, GameState


@pytest.fixture
def no_gamestate_repository(monkeypatch):
    """Mocks an empty database"""

    def create_empty_gamestate_repository(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_empty_gamestate_repository,
    )


@pytest.fixture
def no_gamestate(monkeypatch):
    """Returns a mock start gamestate whenever the database is queried"""

    def create_no_gamestate(*args, **kwargs):
        raise GameStateStoreNotFoundError

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_no_gamestate,
    )


@pytest.fixture
def save_new_gamestate(monkeypatch):
    """Returns a gamestate whenever a gamestate is saved to the database"""

    def create_newly_saved_gamestate(*args, **kwargs):
        gamestate = GameState(
            "alpha",
            shuffle_deck=False,
        )
        gamestate.base_card = Card("2", "D")
        gamestate.is_round_started = False
        gamestate.is_round_ended = True
        return gamestate

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_newly_saved_gamestate,
    )


@pytest.fixture
def update_new_gamestate(monkeypatch):
    """Returns a gamestate whenever a gamestate is saved to the database"""

    def create_newly_saved_gamestate(*args, **kwargs):
        gamestate = GameState(
            "alpha",
            shuffle_deck=False,
        )
        gamestate.base_card = Card("2", "D")
        gamestate.is_round_started = False
        gamestate.is_round_ended = True
        return gamestate

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.update",
        create_newly_saved_gamestate,
    )


@pytest.fixture
def start_gamestate_next_card_higher(monkeypatch):
    """Returns a mock start gamestate whenever the database is queried"""

    def create_mock_gamestate(*args, **kargs):
        gamestate = GameState(
            "alpha",
            shuffle_deck=False,
        )
        gamestate.base_card = Card("7", "D")
        gamestate.deck = Deck([Card("A", "H")])
        gamestate.is_round_started = True
        gamestate.is_round_ended = False
        return gamestate

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_mock_gamestate,
    )

    def create_mock_updated_gamestate_store_repository(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.update",
        create_mock_updated_gamestate_store_repository,
    )


@pytest.fixture
def start_gamestate_next_card_lower(monkeypatch):
    """Returns a mock start gamestate whenever the database is queried"""

    def create_mock_gamestate(*args, **kwargs):
        gamestate = GameState(
            "alpha",
            shuffle_deck=False,
        )
        gamestate.base_card = Card("7", "D")
        gamestate.deck = Deck([Card("2", "H")])
        gamestate.is_round_started = True
        gamestate.is_round_ended = False
        return gamestate

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_mock_gamestate,
    )

    def create_mock_updated_gamestate_store_repository(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.update",
        create_mock_updated_gamestate_store_repository,
    )


@pytest.fixture
def end_gamestate(monkeypatch):
    """Returns a mock end gamestate whenever the database is queried"""

    def create_mock_gamestate(*args, **kwargs):
        return GameStateStore(
            id=1,
            user_id=1,
            gamestate=GameState(
                "alpha",
                shuffle_deck=False,
                is_round_started=False,
                is_round_ended=True,
            ),
        )

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateStoreRepository.get",
        create_mock_gamestate,
    )


@pytest.fixture
def bankrupt_gamestate(monkeypatch):
    """Returns a mock start gamestate whenever the database is queried"""

    def create_bankrupt_gamestate(*args, **kwargs):
        return GameState(
            "alpha",
            shuffle_deck=False,
            money=0,
            is_round_started=False,
            is_round_ended=True,
        )

    monkeypatch.setattr(
        "app.repository.gamestate.GameStateRepository.get",
        create_bankrupt_gamestate,
    )


@pytest.fixture
def unshuffled_deck(monkeypatch):
    """Returns a mock start gamestate whenever the database is queried"""

    def create_mock_gamestate_unshuffled_deck(self, *args, **kwargs):
        self.deck = Deck()

    monkeypatch.setattr(
        "hilo.models.gamestate.GameState.init_deck",
        create_mock_gamestate_unshuffled_deck,
    )

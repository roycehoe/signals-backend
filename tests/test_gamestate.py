import random

import pytest

from hilo.models.card import RANKS, SUITS, Card
from hilo.models.deck import Deck
from hilo.models.gamestate import GameState


@pytest.fixture
def shuffled_deck():
    card_list = [Card(rank, suit) for rank in RANKS for suit in SUITS]
    random.seed(1337)
    random.shuffle(card_list)
    return Deck(card_list)


def test_not_shuffle_deck():
    """Ensures that deck is not shuffled if shuffle deck is False"""

    assert GameState("foo", shuffle_deck=False).deck == Deck()


def test_shuffle_deck(shuffled_deck):
    random.seed(1337)
    assert GameState("foo", shuffle_deck=True).deck == shuffled_deck


def test_method_init_deck_false():
    """Ensures that deck is not shuffled if shuffle in init_deck is False"""

    gamestate = GameState("foo", shuffle_deck=False)
    gamestate.init_deck(shuffle=False)
    assert gamestate.deck == Deck()


def test_method_init_deck_true(shuffled_deck):
    """Ensures that deck is shuffled if shuffle in init_deck is True"""
    random.seed(1337)
    gamestate = GameState("foo", shuffle_deck=False)
    gamestate.init_deck(shuffle=True)
    assert gamestate.deck == shuffled_deck


def test_method_is_bankrupt_not_bankrupt():
    """Ensures that is_bankupt method works for non-bankrupt players"""

    gamestate = GameState("foo", shuffle_deck=False)

    assert not gamestate.money == 0
    assert not gamestate.is_bankrupt()


def test_method_is_bankrupt():
    """Ensures that is_bankupt method works for bankrupt players"""
    gamestate = GameState("foo", shuffle_deck=False, money=0)

    assert gamestate.money == 0
    assert gamestate.is_bankrupt()


def test_method_draw_base_card():
    """Ensures that base card is drawn"""

    gamestate = GameState("foo", shuffle_deck=False)

    gamestate.draw_base_card()
    assert gamestate.base_card == Card("2", "D")


def test_method_draw_next_card():
    """Ensures that next card is drawn"""

    gamestate = GameState("foo", shuffle_deck=False)

    gamestate.draw_next_card()
    assert gamestate.next_card == Card("2", "D")


def test_method_increment_round():
    """Ensures that increment round increases round attribute"""

    gamestate = GameState("foo", shuffle_deck=False)

    assert gamestate.round == 1
    gamestate.increment_round()
    assert gamestate.round == 2

import random

import pytest

from hilo.models.card import RANKS, SUITS, Card
from hilo.models.deck import Deck


@pytest.fixture
def unshuffled_card_list():
    return [Card(rank, suit) for rank in RANKS for suit in SUITS]


@pytest.fixture
def shuffled_card_list():
    card_list = [Card(rank, suit) for rank in RANKS for suit in SUITS]
    random.seed(1337)
    random.shuffle(card_list)
    return card_list


def test_default_card_list(unshuffled_card_list):
    """Ensures cards attribute of Deck contains expected list of cards"""

    assert Deck().cards == unshuffled_card_list


def test_method_shuffle(shuffled_card_list):
    """Ensures deck shuffle method shuffles cards"""

    random.seed(1337)
    test_deck = Deck()
    test_deck.shuffle()

    assert test_deck.cards == shuffled_card_list


def test_eq_with_deck_equal_cards_equal_value_equal_order():
    """Ensures working '==' comparator when first deck object has similar card list"""

    assert Deck([Card("A", "D"), Card("A", "H"), Card("A", "C")]) == Deck(
        [Card("A", "D"), Card("A", "H"), Card("A", "C")]
    )


def test_eq_with_deck_equal_cards_equal_value_unequal_order():
    """Ensures working '==' comparator when first deck object has similar cards in different order"""

    assert not Deck([Card("A", "D"), Card("A", "H"), Card("A", "C")]) == Deck(
        [Card("A", "H"), Card("A", "D"), Card("A", "C")]
    )


def test_eq_with_deck_equal_cards_unequal_value_equal_order():
    """Ensures working '==' comparator when first deck object has similar card count with different values"""

    assert not Deck([Card("A", "D"), Card("A", "H"), Card("A", "S")]) == Deck(
        [Card("A", "H"), Card("A", "D"), Card("A", "C")]
    )


def test_eq_with_deck_more_cards():
    """Ensures working '==' comparator when first deck object has more cards"""

    assert not Deck(
        [Card("A", "D"), Card("A", "H"), Card("A", "C"), Card("A", "S")]
    ) == Deck([Card("A", "H"), Card("A", "D"), Card("A", "C")])


def test_eq_with_deck_less_cards():
    """Ensures working '==' comparator when first deck object has less cards"""

    assert not Deck([Card("A", "D"), Card("A", "H")]) == Deck(
        [Card("A", "H"), Card("A", "D"), Card("A", "C")]
    )

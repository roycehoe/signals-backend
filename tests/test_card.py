import pytest
from frozendict import frozendict

from hilo.errors import CardRankError, CardSuitError
from hilo.models.card import RANKS, SUITS, Card, rank_index, suit_index


def test_RANKS():
    """Ensures module contains RANKS constant"""

    assert RANKS == frozendict(
        {
            "2": "Two",
            "3": "Three",
            "4": "Four",
            "5": "Five",
            "6": "Six",
            "7": "Seven",
            "8": "Eight",
            "9": "Nine",
            "10": "Ten",
            "J": "Jack",
            "Q": "Queen",
            "K": "King",
            "A": "Ace",
        }
    )


def test_SUITS():
    """Ensures module contains SUITS constant"""

    assert SUITS == frozendict(
        {"D": "Diamonds", "C": "Clubs", "H": "Hearts", "S": "Spades"}
    )


def test_rank_index():
    """Ensures rank_index returns expected index value"""

    assert rank_index("2") == 0


def test_suit_index():
    """Ensures suit_index returns expected index value"""

    assert suit_index("D") == 0


def test_rank_index_invalid():
    """Ensures rank_index raises an error upon receiving an invalid key value"""

    with pytest.raises(ValueError):
        rank_index("18")


def test_suit_index_invalid():
    """Ensures suit_index raises an error upon receiving an invalid key value"""

    with pytest.raises(ValueError):
        suit_index("Diamonds")


def test_create_card_rank_invalid():
    """Ensures custom error will be raised if Card object is created with an invalid rank"""

    with pytest.raises(CardRankError) as excinfo:
        Card("King", "C")
    assert "King is not a valid rank!" == str(excinfo.value)


def test_create_card_suit_invalid():
    """Ensures custom error will be raised if Card object is created with an invalid suit"""

    with pytest.raises(CardSuitError) as excinfo:
        Card("K", "Clubs")
    assert "Clubs is not a valid suit!" == str(excinfo.value)


def test_create_card_suit_and_rank_invalid():
    """Ensures custom error raised if Card object is created with an invalid rank and suit"""

    with pytest.raises(CardRankError) as excinfo:
        Card("King", "Clubs")
    assert "King is not a valid rank!" == str(excinfo.value)


def test_gt_with_cards_higher_rank():
    """Ensures working '>' comparator when first Card object has a higher rank"""

    assert Card("10", "H") > Card("9", "H")


def test_gt_with_cards_higher_suit():
    """Ensures working '>' comparator when first Card object has a higher suit"""

    assert Card("A", "C") > Card("A", "D")


def test_gt_with_cards_higher_rank_and_suit():
    """Ensures working '>' comparator when first Card object has a higher rank and suit"""

    assert Card("6", "C") > Card("4", "D")


def test_gt_with_non_card():
    """Ensures custom error raised if Card object is compared with non-Card object with '>' comparator"""

    with pytest.raises(TypeError) as excinfo:
        Card("A", "D") > "10"
    assert "'>' not supported between instances of 'Card' and 'str'" == str(
        excinfo.value
    )


def test_lt_with_cards_lower_rank():
    """Ensures working '<' comparator when first Card object has a lower rank"""

    assert Card("9", "H") < Card("10", "H")


def test_lt_with_cards_lower_suit():
    """Ensures working '<' comparator when first Card object has a lower suit"""

    assert Card("A", "D") < Card("A", "C")


def test_lt_with_cards_lower_rank_and_suit():
    """Ensures working '<' comparator when first Card object has a lower rank and suit"""

    assert Card("4", "D") < Card("6", "C")


def test_lt_with_non_card():
    """Ensures custom error raised if Card object is compared with non-Card object with '<' comparator"""

    with pytest.raises(TypeError) as excinfo:
        Card("A", "D") < "10"
    assert "'<' not supported between instances of 'Card' and 'str'" == str(
        excinfo.value
    )


def test_eq_with_cards_higher_suit():
    """Ensures working '==' comparator when first Card object has a higher suit"""

    assert Card("7", "H") != Card("7", "D")


def test_eq_with_cards_lower_suit():
    """Ensures working '==' comparator when first Card object has a lower suit"""

    assert Card("7", "H") != Card("7", "C")


def test_eq_with_cards_lower_rank():
    """Ensures working '==' comparator when first Card object has a lower rank"""

    assert Card("7", "H") != Card("6", "H")


def test_eq_with_cards_higher_rank():
    """Ensures working '==' comparator when first Card object has a higher rank"""

    assert Card("7", "H") != Card("8", "H")


def test_eq_with_cards_equal_rank_and_suit():
    """Ensures working '==' comparator when first Card object has similar rank and suit"""

    assert Card("5", "S") == Card("5", "S")


def test_eq_with_non_card():
    """Ensures working '==' comparator when first Card object is compared with non-Card object"""

    assert not Card("A", "D") == "10"


def test_card_name():
    """Ensures Card object contains expected name attribute"""

    assert Card("A", "D").name == "Ace of Diamonds"


def test_card_value():
    """Ensures Card object contains expected name attribute"""

    assert Card("A", "D").value == 49


def test_card_static_method_compute_card_value():
    """Ensures compute_card_value static method returns exepcted value"""

    assert Card.compute_card_value("A", "D") == 49

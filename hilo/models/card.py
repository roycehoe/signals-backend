from dataclasses import field
from typing import Optional

from frozendict import frozendict
from pydantic import validator
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from hilo.errors import CardRankError, CardSuitError
from hilo.models.ORMConfig import ORMConfig

RANKS = frozendict(
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
SUITS = frozendict({"D": "Diamonds", "C": "Clubs", "H": "Hearts", "S": "Spades"})


def rank_index(rank):
    return list(RANKS).index(rank)


def suit_index(suit):
    return list(SUITS).index(suit)


@dataclass(order=True, frozen=True)
class Card:
    value: Optional[int] = field(init=False, repr=False, default=None)
    name: Optional[str] = field(init=False, repr=False, default=None)
    rank: str
    suit: str

    def __post_init_post_parse__(self):
        object.__setattr__(self, "value", self.compute_card_value(self.rank, self.suit))
        object.__setattr__(
            self, "name", f"{RANKS.get(self.rank)} of {SUITS.get(self.suit)}"
        )

    @staticmethod
    def compute_card_value(rank, suit):
        return 4 * (rank_index(rank)) + (suit_index(suit) + 1)

    @validator("rank")
    def validate_rank(cls, rank):
        if rank not in RANKS:
            raise CardRankError(f"{rank} is not a valid rank!")
        return rank

    @validator("suit")
    def validate_suit(cls, suit):
        if suit not in SUITS:
            raise CardSuitError(f"{suit} is not a valid suit!")
        return suit


@dataclass(order=True, frozen=True, config=ORMConfig)
class ShowCard:
    rank: str
    suit: str
    name: str

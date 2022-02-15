import random
from typing import List

from pydantic import Field
from pydantic.dataclasses import dataclass

from hilo.models.card import RANKS, SUITS, Card
from hilo.models.ORMConfig import ORMConfig


@dataclass(config=ORMConfig)
class Deck:
    cards: List[Card] = Field(
        default=[Card(rank, suit) for rank in RANKS for suit in SUITS],
    )

    def shuffle(self):
        random.shuffle(self.cards)

    def __eq__(self, other):
        return self.cards == other.cards

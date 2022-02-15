from dataclasses import InitVar, field
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic.types import NonNegativeInt

from hilo.models.card import Card
from hilo.models.deck import Deck
from hilo.models.ORMConfig import ORMConfig


@dataclass(config=ORMConfig)
class GameState:
    player_name: str
    deck: Deck = field(init=False)
    shuffle_deck: InitVar[bool] = field(default=True)
    base_card: Optional[Card] = field(init=False, default=None)
    next_card: Optional[Card] = field(init=False, default=None)
    money: NonNegativeInt = 1000
    round: int = 1
    win: Optional[bool] = field(init=False, default=None)
    is_round_started: bool = False
    is_round_ended: bool = False

    def __post_init__(self, shuffle_deck):
        self.init_deck(shuffle=shuffle_deck)

    def init_deck(self, shuffle=False):
        self.deck = Deck()
        if shuffle:
            self.deck.shuffle()

    def draw_base_card(self, index=0):
        self.base_card = self.deck.cards.pop(index)

    def draw_next_card(self, index=0):
        self.next_card = self.deck.cards.pop(index)

    def is_bankrupt(self):
        return self.money == 0

    def increment_round(self):
        self.round += 1

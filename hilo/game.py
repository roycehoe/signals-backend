from typing import Optional

from pydantic import BaseModel
from pydantic.types import NonNegativeInt, PositiveInt

from hilo.errors import CardComparatorError, InvalidBetError
from hilo.models.card import Card, ShowCard
from hilo.models.gamestate import GameState
from hilo.models.prediction import Prediction

MINIMUM_CARDS_REQUIRED = 2


def init_gamestate(player_name: str) -> GameState:
    gamestate: GameState = GameState(player_name, True)
    gamestate.draw_base_card()
    gamestate.is_round_started = True

    return gamestate


def __prepare_deck(gamestate: GameState) -> GameState:
    if len(gamestate.deck.cards) < MINIMUM_CARDS_REQUIRED:
        gamestate.init_deck(shuffle=True)
    return gamestate


def init_round(gamestate: GameState) -> GameState:
    updated_gamestate: GameState = __prepare_deck(gamestate)

    updated_gamestate.draw_base_card()
    updated_gamestate.increment_round()
    updated_gamestate.is_round_started = True
    updated_gamestate.is_round_ended = False

    return updated_gamestate


def __compute_prediction_result(
    next_card: Optional[Card],
    base_card: Optional[Card],
    prediction: Prediction,
) -> bool:
    if next_card is None or base_card is None:
        raise CardComparatorError

    if prediction is Prediction.HIGHER:
        return next_card > base_card
    return next_card < base_card


def __compute_round_result(gamestate: GameState, prediction: Prediction) -> GameState:
    gamestate.draw_next_card()
    gamestate.win = __compute_prediction_result(
        gamestate.next_card, gamestate.base_card, prediction
    )

    return gamestate


def __validate_bet(bet: PositiveInt, money: NonNegativeInt) -> None:
    if bet > money:
        raise InvalidBetError("Bet amount exceeds player money")


def __update_money(gamestate: GameState, bet: PositiveInt) -> GameState:
    __validate_bet(bet, gamestate.money)
    gamestate.money += bet if gamestate.win else -bet
    return gamestate


def get_round_result(
    gamestate: GameState, prediction: Prediction, bet: PositiveInt
) -> GameState:
    round_result: GameState = __compute_round_result(gamestate, prediction)

    round_result = __update_money(round_result, bet)
    round_result.is_round_ended = True
    round_result.is_round_started = False

    return round_result

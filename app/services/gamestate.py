from pydantic.types import PositiveInt
from sqlalchemy.orm.session import Session

from app import models
from app.errors import (
    GameStateNotFoundError,
    GameStateStoreNotFoundError,
    InvalidBetError,
    RoundNotEndedError,
    RoundNotStartedError,
    UserNotFoundError,
)
from app.repository.gamestate import GameStateRepository
from app.repository.gamestatestore import GameStateStoreRepository
from app.repository.user import UserRepository
from hilo.errors import CardComparatorError
from hilo.game import get_round_result, init_gamestate, init_round
from hilo.models.gamestate import GameState
from hilo.models.prediction import Prediction


def __compute_new_round(user_id: str, session: Session) -> GameState:
    """Computes the new round gamestate from the user's latest gamestate

    :param user_id: The user_id of the user
    :type user_id: str
    :param session: the daabase containing all gamestate and user information
    :type session: Session
    :return: The computed gamestate
    :rtype: GameState
    :raises GameStateNotFoundError: if the user with "user_id" does not have an associated
    gamestate
    :raises RoundNotEndedError: if the user attempts to start a round without
    ending the current round
    """

    try:
        gamestate = GameStateRepository(session).get(user_id)
    except AttributeError:
        raise GameStateNotFoundError("Gamestate not found")

    if not gamestate.is_round_ended:
        raise RoundNotEndedError("Round has not ended")

    updated_gamestate = init_round(gamestate)
    return GameStateRepository(session).update(updated_gamestate, user_id)


def __create_game(user_id: str, session: Session) -> GameState:
    """Creates a new game of hilo and saves it to the database for the user

    :param user_id: The user_id of the user
    :type user_id: str
    :param session: the database containing all gamestate and user information
    :type session: Session
    :return: The computed gamestate
    :rtype: GameState
    :raises UserNotFoundError: if no users with the associated "user_id" can
    be found in "session"
    """

    try:
        username = UserRepository(session).get(id=user_id).username
    except AttributeError:
        raise UserNotFoundError("User with user_id not found")

    new_gamestatestore = models.GameStateStore(
        gamestate=init_gamestate(username), user_id=user_id
    )

    return GameStateStoreRepository(session).save(new_gamestatestore).gamestate


def __restart_gamestate(user_id: str, session: Session) -> GameState:
    """Updates the latest user hilo gamestate with a new GameState instance

    :param user_id: The user_id of the user
    :type user_id: str
    :param session: the database containing all gamestate and user information
    :type session: Session
    :return: The computed gamestate
    :rtype: GameState
    :raises UserNotFoundError: if no users with the associated "user_id" can
    be found in "session"
    """
    try:
        username = UserRepository(session).get(id=user_id).username
    except AttributeError:
        raise UserNotFoundError("User with user_id not found")

    restarted_gamestate = init_gamestate(username)

    return GameStateRepository(session).update(restarted_gamestate, user_id)


def start_round(user_id: str, session: Session) -> GameState:
    """Starts a new round of hilo

    :param user_id: The user_id of the user
    :type user_id: str
    :param session: the database containing all gamestate and user information
    :type session: Session
    :return: The computed gamestate
    :rtype: GameState
    """
    try:
        gamestate: GameState = GameStateRepository(session).get(user_id)

        if not gamestate.is_bankrupt():
            return __compute_new_round(user_id, session)
        return __restart_gamestate(user_id, session)

    except GameStateStoreNotFoundError:
        return __create_game(user_id, session)
    except UserNotFoundError:
        raise UserNotFoundError
    except RoundNotEndedError:
        raise RoundNotEndedError


def end_round(
    user_id: str, session: Session, prediction: Prediction, bet: PositiveInt
) -> GameState:
    """Ends a round of hilo

    :param user_id: The user_id of the user
    :type user_id: str
    :param session: the database containing all gamestate and user information
    :type session: Session
    :param prediction: The user's prediction if the next_card will be higher
    or lower than the base_card
    :type prediction: Prediction
    :param bet: The user's bet on their prediction
    :return: The computed gamestate
    :rtype: GameState
    :raises GameStateNotFoundError: if the user with "user_id" does not have an associated
    gamestate
    :raises RoundNotStartedError: if users attempt to end a round without starting a round
    :raises CardComparatorError: if base_card or next_card is of type None
    """

    try:
        gamestate: GameState = GameStateRepository(session).get(user_id)
    except GameStateNotFoundError:
        raise GameStateNotFoundError("gamestate not found")

    if not gamestate.is_round_started:
        raise RoundNotStartedError("Round not started")

    try:
        updated_gamestate = get_round_result(gamestate, prediction, bet)
    except CardComparatorError:
        raise CardComparatorError
    except InvalidBetError:
        raise InvalidBetError

    GameStateRepository(session).update(updated_gamestate, user_id)
    return updated_gamestate

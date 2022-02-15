from typing import Optional

from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from pydantic.class_validators import validator
from pydantic.types import NonNegativeInt, PositiveInt, SecretStr
from starlette import status

from app.errors import INVALID_BET
from hilo.errors import InvalidBetError
from hilo.models.gamestate import GameState
from hilo.models.prediction import Prediction


class UserIn(BaseModel):
    """A request body to create users

    :param username: The new user's username
    :type username: str, max_length=128
    :param password: The new user's password
    :type password: str, max_length=128
    """

    username: str = Field(max_length=128)
    password: str = Field(max_length=128)


class UserOut(BaseModel):
    """A response body after users have been successfully created

    :param username: The new user's username
    :type username: str
    """

    username: str

    class Config:
        orm_mode = True


class GameStateStorageOut(BaseModel):
    """A response body containing all gamestate and meta-gamestate information

    :param id: The gamestate id
    :type round_info: int
    :param user_id: The user_id associated with the gamestate id
    :type round_info: int
    :param gamestate: A pydantic BaseClass containing all information about the current round of hilo
    """

    id: int
    user_id: int
    gamestate: GameState

    class Config:
        orm_mode = True


class HiloChoicesIn(BaseModel):
    """A request body for users to input their game choices for a round of hilo

    :param prediction: The user's choice on whether the base_card will be higher or lower
    than next_card
    :type prediction: Prediction
    :param bet: The user's bet on their prediction
    :type bet: PositiveInt
    """

    prediction: Prediction
    bet: PositiveInt = 1

    @validator("bet", pre=True)
    def invalid_bet(cls, bet):
        """Ensures that bet is an integer and is more than 1
        :raises InvalidBetError: if bet is a non-integer or less than 1
        """

        if not isinstance(bet, int) or bet < 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": INVALID_BET,
                },
            )

        return bet


class LoginIn(BaseModel):
    """A request body for users to key in their credentials

    :param username: The user's username
    :type username: SecretStr
    :param password: The user's password
    :type password: SecretStr
    """

    username: SecretStr = Field(max_length=128)
    password: SecretStr = Field(max_length=128)


class TokenOut(BaseModel):
    """A respose body for a successfully created JWT token

    :param access_token: The JWT access token
    :type access_token: str
    :param token_type: A description of the token type
    :type token_type: str
    """

    access_token: str
    token_type: str


class CardOut(BaseModel):
    """A respose body for a card

    :param rank: The card's rank
    :type rank: str
    :param suit: The card's suit
    :type suit: str
    :param name: The card's full name
    :type name: str
    """

    rank: str
    suit: str
    name: str


class GameStateStartOut(BaseModel):
    """A response body when users start a game of hilo

    :param player_name: The name of the user
    :type player_name: str
    :param money: The amount of money the user currently has
    :type money: NonNegativeInt
    :param round: The total number of round of hilo played by the user
    :type round: int
    :param base_card: The base card drawn by the player, which will be later used
    to compare with the next_card
    :type base_card: Optional[CardOut]
    """

    player_name: str
    money: NonNegativeInt
    round: int
    base_card: Optional[CardOut]


class GameStateEndOut(GameStateStartOut):
    """A response body when users end a game of hilo

    :param next_card: The card drawn by the player at the end of the round, which
    is compared with the base card
    :type next_card: Optional[CardOut]
    :param win: The result for the current round of hilo
    :type win: Optional[bool]
    """

    next_card: Optional[CardOut]
    win: Optional[bool]

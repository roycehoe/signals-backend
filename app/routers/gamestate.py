from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.errors import (
    GAME_NOT_CREATED,
    INVALID_BET,
    INVALID_CARD_COMPARISON_ERROR,
    MISSING_AUTHENTICATION_TOKEN,
    ROUND_NOT_ENDED,
    ROUND_NOT_STARTED,
    TOKEN_AUTHENTICATION_FAILED,
    USER_NOT_FOUND,
    GameStateNotFoundError,
    GameStateStoreNotFoundError,
    InvalidAuthenticationTokenError,
    MissingAuthenticationTokenError,
    RoundNotEndedError,
    RoundNotStartedError,
    UserNotFoundError,
)
from app.repository.gamestate import GameStateRepository
from app.schemas import GameStateEndOut, GameStateStartOut
from app.services import gamestate
from app.token import get_user_id
from hilo.errors import CardComparatorError, InvalidBetError

router = APIRouter(
    tags=["game"],
    prefix="/game",
    dependencies=[Depends(get_session)],
)


@router.get("/info", status_code=status.HTTP_200_OK, response_model=GameStateStartOut)
def get_latest_gamestate(
    token: str = Header(None),
    session: Session = Depends(get_session),
):
    """Gets a user's latest gamestate

    :param token: The JWT access token containing the user's user_id
    :type token: str
    :param session: The database containing the user's latest gamestate
    :type session: Session
    :returns: The user's latest gamestate
    :rtype: schemas.GameStateStartOut
    :raises HTTPException: if token or gamestate validation fails
    """

    try:
        user_id = get_user_id(token)
    except MissingAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": MISSING_AUTHENTICATION_TOKEN},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": TOKEN_AUTHENTICATION_FAILED},
        )
    except InvalidAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": TOKEN_AUTHENTICATION_FAILED},
        )

    try:
        return GameStateRepository(session).get(user_id)

    except GameStateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": GAME_NOT_CREATED},
        )
    except GameStateStoreNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": GAME_NOT_CREATED},
        )


@router.get(
    "/game",
    status_code=status.HTTP_201_CREATED,
    response_model=GameStateStartOut,
)
def start_round(
    token: str = Header(None),
    session: Session = Depends(get_session),
):
    """Creates a new hilo game for bankrupted users or new users, and creates a new round of hilo

    :param token: The JWT access token containing the user's user_id
    :type token: str
    :param session: The database containing the user's latest gamestate
    :type session: Session
    :returns: The gamestate information of a new round
    :rtype: schemas.GameStateResponse
    :raises HTTPException: if token or gamestate validation fails
    """
    try:
        user_id = get_user_id(token)
    except MissingAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": MISSING_AUTHENTICATION_TOKEN,
            },
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": TOKEN_AUTHENTICATION_FAILED,
            },
        )
    except InvalidAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": TOKEN_AUTHENTICATION_FAILED},
        )

    try:
        return gamestate.start_round(user_id, session)

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": USER_NOT_FOUND,
            },
        )
    except RoundNotEndedError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": ROUND_NOT_ENDED},
        )


@router.post("/play", status_code=status.HTTP_200_OK, response_model=GameStateEndOut)
def end_round(
    request: schemas.HiloChoicesIn,
    token: str = Header(None),
    session: Session = Depends(get_session),
):
    """Concludes a game of hilo based on user's choices

    :param request: The user's in-game choices for the current round of hilo
    :type request: schemas.HiloChoicesIn
    :param token: The JWT access token containing the user's user_id
    :type token: str
    :param session: The database containing the user's latest gamestate
    :type session: Session
    :returns: The gamestate information of a new round
    :rtype: schemas.GameStateResponse
    :raises HTTPException: if token, gamestate, or "request" validation fails
    """

    try:
        user_id = get_user_id(token)
    except MissingAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": MISSING_AUTHENTICATION_TOKEN,
            },
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": TOKEN_AUTHENTICATION_FAILED,
            },
        )
    except InvalidAuthenticationTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": TOKEN_AUTHENTICATION_FAILED},
        )

    try:
        return gamestate.end_round(user_id, session, request.prediction, request.bet)
    except GameStateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": GAME_NOT_CREATED,
            },
        )
    except GameStateStoreNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": GAME_NOT_CREATED},
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": USER_NOT_FOUND,
            },
        )
    except RoundNotStartedError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": ROUND_NOT_STARTED,
            },
        )
    except InvalidBetError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": INVALID_BET,
            },
        )
    except CardComparatorError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": INVALID_CARD_COMPARISON_ERROR,
            },
        )

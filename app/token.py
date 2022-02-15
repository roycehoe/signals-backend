from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.errors import InvalidAuthenticationTokenError, MissingAuthenticationTokenError


def create_access_token(data: dict) -> str:
    """Converts a dictionary to a JWT access token

    :param data: A dictionary containing data to encode into a JWT access token
    :type data: dict
    :returns: A JWT token based on param data
    :rtype: str
    """

    raw_token_data = data.copy()
    token_expiry_time = datetime.utcnow() + timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    raw_token_data.update({"exp": token_expiry_time})
    encoded_jwt = jwt.encode(raw_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_token(token: str) -> None:
    """Authenticates a JWT token

    :param token: A JWT token
    :type token: str
    :returns: None
    :rtype: None
    :raises JWTError: If token decoding fails
    :raises InvalidAuthenticationTokenError: If token does not have a "username" key
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError

    try:
        payload["username"]
    except KeyError:
        raise InvalidAuthenticationTokenError


def get_username(token: str) -> str:
    """Decodes and gets username value stored within a JWT token

    :param token: A JWT token
    :type token: str
    returns: username value stored within a JWT token
    :rtype: str
    :raises JWTError: If token decoding fails
    :raises MissingAuthenticationTokenError: If no authentication token is given
    :raises InvalidAuthenticationTokenError: If token does not have a "username" key
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError
    except AttributeError:
        raise MissingAuthenticationTokenError

    try:
        username: str = payload["username"]
    except KeyError:
        raise InvalidAuthenticationTokenError

    return username


def get_user_id(token: str) -> str:
    """Decodes and gets user_id stored within a JWT token

    :param token: A JWT token
    :type token: str
    returns: user_id stored within a JWT token
    :rtype: str
    :raises JWTError: If token decoding fails
    :raises MissingAuthenticationTokenError: If no authentication token is given
    :raises InvalidAuthenticationTokenError: If token does not have a "username" key
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError
    except AttributeError:
        raise MissingAuthenticationTokenError

    try:
        user_id: str = payload["user_id"]
    except KeyError:
        raise InvalidAuthenticationTokenError

    return user_id

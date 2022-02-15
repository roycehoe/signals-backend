import secrets
from typing import Optional

from dotenv import dotenv_values

config = dotenv_values(".env")

DEFAULT_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = "2880"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


def __create_secret_key() -> str:
    """Creates a secret key based on randomly generated ASCII characters

    :returns: A secret key
    :rtype: str
    """

    ascii_chars = [chr(i) for i in range(128)]
    return "".join(secrets.choice(ascii_chars) for i in range(32))


def __get_token_variable(env_value: Optional[str], default_value: str) -> str:
    """Helps to set token variables

    :param env_value: A function to get an environment variable
    :type env_value: Optional[str]
    :param default_value: The default value should env_value be None
    :type default_value: str
    :returns: A token variable
    :rtype: str
    """

    return env_value if env_value else default_value


SECRET_KEY = __get_token_variable(config.get("SECRET_KEY"), __create_secret_key())
ALGORITHM = __get_token_variable(config.get("ALGORITHM"), DEFAULT_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = __get_token_variable(
    config.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
)

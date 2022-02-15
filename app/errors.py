USER_NOT_FOUND = "USER_NOT_FOUND"
GAME_NOT_CREATED = "GAME_NOT_CREATED"
TOKEN_AUTHENTICATION_FAILED = "TOKEN_AUTHENTICATION_FAILED"
USERNAME_TAKEN = "USERNAME_TAKEN"
ROUND_NOT_ENDED = "ROUND_NOT_ENDED"
ROUND_NOT_STARTED = "ROUND_NOT_STARTED"
INVALID_BET = "INVALID_BET"
INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
INVALID_CARD_COMPARISON_ERROR = "INVALID_CARD_COMPARISON_ERROR"
REQUEST_MAXIMUM_LENGTH_EXCEEDED = "REQUEST_MAXIMUM_LENGTH_EXCEEDED"
UNKNOWN_ERROR_OCCURRED = "UNKNOWN_ERROR_OCCURRED"
TYPE_VALIDATION_ERROR = "TYPE_VALIDATION_ERROR"
MISSING_AUTHENTICATION_TOKEN = "MISSING_AUTHENTICATION_TOKEN"
MISSING_FIELD_VALUES = "MISSING_FIELD_VALUES"
MALFORMED_REQUEST_ERROR = "MALFORMED_REQUEST_ERROR"


class UserNotFoundError(Exception):
    """Exception raised when no users be found when querrying a database"""

    pass


class UsernameNotUniqueError(Exception):
    """Exception raised when a non-unique username is added to the database"""

    pass


class GameStateNotFoundError(Exception):
    """Exception raised when the queried gamestate cannot be found in the database"""

    pass


class GameStateStoreNotFoundError(Exception):
    """Exception raised when the queried gamestatestore cannot be found in the database"""

    pass


class RoundNotEndedError(Exception):
    """Exception raised when users attempt to start a round without ending the current round"""

    pass


class RoundNotStartedError(Exception):
    """Exception raised when users attempt to end a round without starting a round"""

    pass


class InvalidCredentialsError(Exception):
    """Exception raised when users attempt to log in with invalid credentials"""

    pass


class MissingAuthenticationTokenError(Exception):
    """Exception raised when users are missing an authentication token"""

    pass


class InvalidAuthenticationTokenError(Exception):
    """Exception raised when users use an invalid authentication token"""

    pass


class InvalidBetError(Exception):
    """Exception raised if user's bet is not an integer or less than 1"""

    pass


class InvalidUserQueryError(Exception):
    """Exception raised for invalid query to the user database table"""

    pass


class TypeErrorUndefined(Exception):
    pass

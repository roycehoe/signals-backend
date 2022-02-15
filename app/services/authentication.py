from sqlalchemy.orm import Session

from app import models, schemas
from app.errors import InvalidCredentialsError, InvalidUserQueryError, UserNotFoundError
from app.hashing import verify_password
from app.repository.user import UserRepository
from app.token import create_access_token


def __authenticate_user(user: models.User, password: str) -> None:
    """Authenticates a user with a username and password combination

    :param user: The user information that will be verified against a given password string
    :type user: models.User
    :param password: The password string that will be verified against a given user information
    :type password: str
    :returns: None if user passes all authentication checks
    :rtype: None
    :raises InvalidCredentialsError: If users key in invalid credentials into "user"
    """

    if not user or not verify_password(password, user.password):
        raise InvalidCredentialsError("Invalid credentials")


def get_access_token(
    request: schemas.UserIn,
    session: Session,
) -> schemas.TokenOut:
    """Returns a JWT token to an authenticated user

    :param request: A request body which takes in a username and password
    :type request: schemas.UserIn
    :param session: The database which contains all authenticated username/password values
    :type session: Session
    :returns: A JWT token
    :rtype: schemas.TokenOut
    """

    try:
        user = UserRepository(session).get(username=request.username)
    except UserNotFoundError:
        raise UserNotFoundError
    except InvalidUserQueryError:
        raise InvalidUserQueryError

    try:
        __authenticate_user(user, request.password)
    except InvalidCredentialsError:
        raise InvalidCredentialsError

    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username}
    )

    return schemas.TokenOut(access_token=access_token, token_type="bearer")

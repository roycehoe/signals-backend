from time import time

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.errors import UsernameNotUniqueError
from app.hashing import hash_password
from app.repository.user import UserRepository


def create_user(request: schemas.UserIn, session: Session) -> models.User:
    """Creates and stores a new user in a database

    :param request: The request body for users to input their new account credentials
    :type: schemas.UserIn
    :param session: The database that user's credentials are uploaded to
    :type session: Session
    :returns: Full details of the created user
    :rtype: models.User
    raises UsernameNotUniqueError: if username in request.username is already taken
    in the session database
    """

    new_user = models.User(
        username=request.username,
        password=hash_password(request.password),
        created_at=time(),
    )

    try:
        UserRepository(session).save(new_user)
    except UsernameNotUniqueError:
        raise UsernameNotUniqueError

    return new_user

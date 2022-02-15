from typing import Union

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.session import Session

from app import models
from app.errors import InvalidUserQueryError, UsernameNotUniqueError, UserNotFoundError


class UserRepository:
    """Holds CRUD methods for the user database table

    :param session: The database session
    :type session: Session
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: models.User) -> models.User:
        """Adds a new user to the user database table

        :param user: The user model that should be added to the database
        :type user: models.User
        :return: The added user model
        :rtype: models.User
        """
        try:
            self.session.add(user)
            self.session.commit()
            return user

        except IntegrityError:
            raise UsernameNotUniqueError

    def get(self, **filters: Union[str, int]) -> models.User:
        """Gets a user from the user database table

        :param filters: kwargs for the user_id or username, used as a filter to get
        the corresponding "models.User"
        :type filters: Union[str, int]
        :return: The user model obtained from the database
        :rtype: models.User
        :raises InvalidUserQueryError: If invalid kwargs are used
        :raises UserNotFoundError: If no users with the defined kwargs can be found
        within the database
        """

        try:
            if user := self.session.query(models.User).filter_by(**filters).first():
                return user
        except InvalidRequestError:
            raise InvalidUserQueryError("Invalid kwarg for **filters")

        raise UserNotFoundError

from sqlalchemy.orm.session import Session

from app import models
from app.errors import GameStateStoreNotFoundError


class GameStateStoreRepository:
    """Holds CRUD methods for the gamestate database table

    :param session: The database session
    :type session: Session
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, gamestatestore: models.GameStateStore) -> models.GameStateStore:
        """Adds a gamestatestore model to the gamestate database table

        :param user: The gamestatestore model that should be added to the gamestate database
        :type user: models.GameStateStore
        :return: The added gamestate model
        :rtype: models.GameStateStore
        """

        self.session.add(gamestatestore)
        self.session.commit()
        return gamestatestore

    def get(self, user_id: str) -> models.GameStateStore:
        """Gets a gamestatestore model from the gamestate database table

        :param user_id: The gamestatestore model that should be returned from the gamestate database
        with the associated user_id
        :type user_id: str
        :return: The requested gamestate model
        :rtype: models.GameStateStore
        :raises GameStateStoreNotFoundError: If no GameStateStore can be found with the given user_id
        """

        if gamestatestore := (
            self.session.query(models.GameStateStore).filter_by(user_id=user_id).first()
        ):
            return gamestatestore

        raise GameStateStoreNotFoundError("Gamestatestore not found")

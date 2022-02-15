from typing import Optional

from sqlalchemy.orm.session import Session

from app import models
from app.errors import GameStateNotFoundError
from app.repository.gamestatestore import GameStateStoreRepository
from hilo.models.gamestate import GameState


class GameStateRepository:
    """Holds CRUD methods for attribute gamestate within the gaestate database table

    :param session: The database session
    :type session: Session
    """

    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: str) -> GameState:
        """Gets a user's GameState from the gamestate database table

        :param user_id: The GameState that should be returned from the gamestate database
        with the associated user_id
        :type user_id: str
        :return: The requested GameState
        :rtype: GameState
        :raises GameStateNotFoundError: If no GameState can be found with the given user_id
        """

        try:
            return GameStateStoreRepository(self.session).get(user_id).gamestate
        except AttributeError:
            raise GameStateNotFoundError("Gamestate not found")

    def update(self, updated_gamestate: GameState, user_id: str) -> GameState:
        """Updates a user's GameState from the gamestate database table

        :param user_id: The GameState that should be updated from the gamestate database
        with the associated user_id
        :type user_id: str
        :return: The updated GameState
        :rtype: GameState
        :raises GameStateNotFoundError: If no GameState can be found with the given user_id
        """

        gamestatestore = GameStateStoreRepository(self.session).get(user_id)

        if gamestatestore.gamestate:
            gamestatestore.gamestate = updated_gamestate
            self.session.commit()
            return gamestatestore.gamestate

        raise GameStateNotFoundError("Gamestate not found")

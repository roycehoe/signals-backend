from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.sqltypes import Float, PickleType

from app.database import Base


class User(Base):
    """Creates a table with an SQLAlchemy model to store user information

    :attr __tablename__: The name of the table, "user"
    :type __tablename__: str
    :param id: Creates a column named "id" to store the id of each user
    :type id: Integer
    :param username: Creates a column named "username" to store the username
    of each user associated with each "id"
    :type username: String
    :param username: Creates a column named "password" to store the
    password of each user associated with each "id"
    :type id: String
    :param id: Creates a column named "created_at" to store the time of
    creation for each user associated with each "id"
    :type id: Float
    """

    __tablename__ = "user"

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(Float)

    gamestate: RelationshipProperty = relationship(
        "GameStateStore", back_populates="user"
    )


class GameStateStore(Base):
    """Creates a table with an SQLAlchemy model to store gamestate information

    :attr __tablename__: The name of the table, "gamestate"
    :type __tablename__: str
    :param id: Creates a column named "id" to store the id of each gamestate
    :type id: Integer
    :param user_id: Creates a column named "user_id" to store user_ids associated
    with each "id"
    :type username: Integer
    :param gamestate: Creates a column named "gamestate" to store all
    gamestate information associated with each "id"
    :type gamestate: PickleType
    """

    __tablename__ = "gamestate"

    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    gamestate = Column(PickleType)

    user: RelationshipProperty = relationship("User", back_populates="gamestate")

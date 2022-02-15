import random
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from hilo.models.card import RANKS, SUITS, Card
from hilo.models.deck import Deck

client = TestClient(app)


@pytest.fixture
def unshuffled_card_list():
    return [Card(rank, suit) for rank in RANKS for suit in SUITS]


@pytest.fixture
def shuffled_card_list():
    card_list = [Card(rank, suit) for rank in RANKS for suit in SUITS]
    random.seed(1337)
    random.shuffle(card_list)
    return card_list

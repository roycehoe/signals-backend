import pytest


@pytest.fixture
def valid_token(monkeypatch):
    """Returns a mock user whenever the database is queried"""
    pass


@pytest.fixture
def token_expiry(monkeypatch):
    """Returns a mock user whenever the database is queried"""

    monkeypatch.setattr("app.config.ACCESS_TOKEN_EXPIRE_MINUTES", "2880")

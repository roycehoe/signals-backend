import pytest

from app.errors import UsernameNotUniqueError
from app.models import User


@pytest.fixture
def mock_user(monkeypatch):
    """Returns a mock user whenever the database is queried"""

    def create_mock_user(*args, **kwargs):
        return User(
            id=1,
            username="alpha",
            password="$2b$12$ky3dtAnRrCh3IHWNEwaBROTJ5tEwzGXR0OtqwoCV44hdXcsy.BAcO",
            created_at=3.1415,
        )

    monkeypatch.setattr(
        "app.repository.user.UserRepository.get",
        create_mock_user,
    )


@pytest.fixture
def mock_no_user(monkeypatch):
    """Returns no user whenever the database is queried"""

    def create_mock_user(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "app.repository.user.UserRepository.get",
        create_mock_user,
    )


@pytest.fixture
def user_creation_success(monkeypatch):
    """Returns valid user when user is saved to database"""

    def create_mock_user(*args, **kwargs):
        return User(
            id=1,
            username="alpha",
            password="$2b$12$ky3dtAnRrCh3IHWNEwaBROTJ5tEwzGXR0OtqwoCV44hdXcsy.BAcO",
            created_at=3.1415,
        )

    monkeypatch.setattr(
        "app.repository.user.UserRepository.save",
        create_mock_user,
    )


@pytest.fixture
def user_creation_failure(monkeypatch):
    """Raises expected error when users fail to be saved to database"""

    def create_mock_failed_user(*args, **kwargs):
        raise UsernameNotUniqueError

    monkeypatch.setattr(
        "app.repository.user.UserRepository.save",
        create_mock_failed_user,
    )

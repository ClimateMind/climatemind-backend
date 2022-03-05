import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client

import pytest
from api.api import app, get_current_user
from fastapi.testclient import TestClient


@pytest.fixture
def authorized_client():

    test_user = {"id": 1, "name": "test", "hashed_password": "super_secret_hashed_super_password!@#23", "email": "test@email.com", "google_id": None, "image_source": "test"}

    app.dependency_overrides[get_current_user] = lambda: test_user

    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides = {}


@pytest.fixture
def unauthorized():

    test_client_without_token = TestClient(app)
    return test_client_without_token

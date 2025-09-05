import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
from app.models.user import User
from app.core.config import settings

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_db():
    # Setup: clean up the user before the test
    User.objects(email="testuser2@example.com").delete()
    yield
    # Teardown: clean up the user after the test
    User.objects(email="testuser2@example.com").delete()

def test_signup(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "testuser2@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "birth_details": {
                "date": "2000-01-01",
                "time": "12:00",
                "location": "New York, NY"
            }
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
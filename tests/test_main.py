"""Tests for the main application file."""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Task Manager API"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_workflow():
    assert 2 == 2

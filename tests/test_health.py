import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_content_type(client: TestClient):
    """Test that health endpoint returns JSON content type."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"] 
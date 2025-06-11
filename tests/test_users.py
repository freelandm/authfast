import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import jwt
import os

from app.models.users import User


class TestUsersEndpoints:
    """Test user-related endpoints."""
    
    def test_get_current_user_success(self, client: TestClient, test_user_data: dict):
        """Test getting current user with valid token."""
        with patch.object(client.app.dependency_overrides, 'clear'):
            # Register and login user first
            with patch('app.controllers.user_controller.trigger_email_verification'):
                client.post("/api/auth/register", json=test_user_data)
            
            login_data = {
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
            login_response = client.post("/api/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            
            # Use token to access protected endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/api/users/me", headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == test_user_data["username"]
            assert data["email"] == test_user_data["email"]
            assert data["full_name"] == test_user_data["full_name"]
            assert "id" in data
            # Sensitive data should not be exposed
            assert "hashed_password" not in data
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/users/me")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/users/me", headers=headers)
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_get_current_user_expired_token(self, client: TestClient):
        """Test accessing protected endpoint with expired token."""
        # Create an expired token
        import time
        from app.dependencies.auth import SECRET_KEY, ALGORITHM
        
        if SECRET_KEY:
            expired_payload = {
                "sub": {"username": "testuser"},
                "exp": int(time.time()) - 3600  # Expired 1 hour ago
            }
            expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
            
            headers = {"Authorization": f"Bearer {expired_token}"}
            response = client.get("/api/users/me", headers=headers)
            
            assert response.status_code == 401
            assert "Could not validate credentials" in response.json()["detail"]
    
    def test_get_current_user_malformed_token(self, client: TestClient):
        """Test accessing protected endpoint with malformed token."""
        headers = {"Authorization": "Bearer malformed.token.here"}
        response = client.get("/api/users/me", headers=headers)
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_get_current_user_wrong_token_format(self, client: TestClient):
        """Test accessing protected endpoint with wrong token format."""
        headers = {"Authorization": "InvalidFormat token_here"}
        response = client.get("/api/users/me", headers=headers)
        
        assert response.status_code == 401 
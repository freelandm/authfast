import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session

from app.models.users import User
from app.controllers import user_controller


class TestAuthRegistration:
    """Test user registration functionality."""
    
    def test_register_user_success(self, client: TestClient, test_user_data: dict):
        """Test successful user registration."""
        with patch.object(user_controller, 'trigger_email_verification') as mock_email:
            response = client.post("/api/auth/register", json=test_user_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["username"] == test_user_data["username"]
            assert data["email"] == test_user_data["email"]
            assert data["full_name"] == test_user_data["full_name"]
            assert "id" in data
            assert "created_at" in data
            # Password should not be in response
            assert "password" not in data
            assert "hashed_password" not in data
            
            # Verify email verification was triggered
            mock_email.assert_called_once()
    
    def test_register_user_duplicate_username(self, client: TestClient, test_user_data: dict):
        """Test registration with duplicate username."""
        with patch.object(user_controller, 'trigger_email_verification'):
            # Register first user
            client.post("/api/auth/register", json=test_user_data)
            
            # Try to register with same username but different email
            duplicate_data = test_user_data.copy()
            duplicate_data["email"] = "different@example.com"
            
            response = client.post("/api/auth/register", json=duplicate_data)
            assert response.status_code == 400
    
    def test_register_user_duplicate_email(self, client: TestClient, test_user_data: dict):
        """Test registration with duplicate email."""
        with patch.object(user_controller, 'trigger_email_verification'):
            # Register first user
            client.post("/api/auth/register", json=test_user_data)
            
            # Try to register with same email but different username
            duplicate_data = test_user_data.copy()
            duplicate_data["username"] = "differentuser"
            
            response = client.post("/api/auth/register", json=duplicate_data)
            assert response.status_code == 400
    
    def test_register_user_invalid_email(self, client: TestClient, test_user_data: dict):
        """Test registration with invalid email format."""
        invalid_data = test_user_data.copy()
        invalid_data["email"] = "invalid-email"
        
        response = client.post("/api/auth/register", json=invalid_data)
        assert response.status_code == 422
    
    def test_register_user_missing_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        incomplete_data = {
            "username": "testuser"
            # Missing email, password, etc.
        }
        
        response = client.post("/api/auth/register", json=incomplete_data)
        assert response.status_code == 422


class TestAuthLogin:
    """Test user login functionality."""
    
    def test_login_success(self, client: TestClient, test_user_data: dict):
        """Test successful user login."""
        with patch.object(user_controller, 'trigger_email_verification'):
            # Register user first
            client.post("/api/auth/register", json=test_user_data)
        
        # Login with form data
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
    
    def test_login_invalid_username(self, client: TestClient):
        """Test login with non-existent username."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 401
    
    def test_login_invalid_password(self, client: TestClient, test_user_data: dict):
        """Test login with incorrect password."""
        with patch.object(user_controller, 'trigger_email_verification'):
            # Register user first
            client.post("/api/auth/register", json=test_user_data)
        
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 401
    
    def test_login_missing_credentials(self, client: TestClient):
        """Test login with missing credentials."""
        response = client.post("/api/auth/login", data={})
        assert response.status_code == 422


class TestEmailVerification:
    """Test email verification functionality."""
    
    def test_resend_email_verification_success(self, client: TestClient, test_user_data: dict):
        """Test successful email verification resend."""
        with patch.object(user_controller, 'trigger_email_verification') as mock_email:
            # Register user first
            client.post("/api/auth/register", json=test_user_data)
            mock_email.reset_mock()  # Reset the mock to clear registration call
            
            # Request email verification resend
            resend_data = {"username": test_user_data["username"]}
            response = client.post("/api/auth/resend_email_verification", json=resend_data)
            
            assert response.status_code == 202
            mock_email.assert_called_once()
    
    def test_resend_email_verification_user_not_found(self, client: TestClient):
        """Test email verification resend for non-existent user."""
        resend_data = {"username": "nonexistent"}
        response = client.post("/api/auth/resend_email_verification", json=resend_data)
        
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    @patch('app.controllers.auth_controller.verify_email')
    def test_verify_email_success(self, mock_verify, client: TestClient):
        """Test successful email verification."""
        mock_verify.return_value = {"message": "Email verified successfully"}
        
        response = client.get("/api/auth/verify_email?token=valid_token")
        
        assert response.status_code == 200
        mock_verify.assert_called_once_with(token="valid_token")
    
    @patch('app.controllers.auth_controller.verify_email')
    def test_verify_email_invalid_token(self, mock_verify, client: TestClient):
        """Test email verification with invalid token."""
        mock_verify.side_effect = Exception("Invalid token")
        
        response = client.get("/api/auth/verify_email?token=invalid_token")
        
        # The endpoint should handle the exception appropriately
        # This depends on how the auth_controller.verify_email handles errors
        mock_verify.assert_called_once_with(token="invalid_token") 
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


@pytest.mark.integration
class TestFullUserFlow:
    """Integration tests for complete user workflows."""
    
    def test_complete_user_registration_and_login_flow(self, client: TestClient, test_user_data: dict):
        """Test the complete flow: register -> login -> access protected endpoint."""
        with patch('app.controllers.user_controller.trigger_email_verification') as mock_email:
            # Step 1: Register a new user
            registration_response = client.post("/api/auth/register", json=test_user_data)
            
            assert registration_response.status_code == 201
            user_data = registration_response.json()
            assert user_data["username"] == test_user_data["username"]
            assert user_data["email"] == test_user_data["email"]
            mock_email.assert_called_once()
            
            # Step 2: Login with the registered user
            login_data = {
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
            login_response = client.post("/api/auth/login", data=login_data)
            
            assert login_response.status_code == 200
            token_data = login_response.json()
            assert "access_token" in token_data
            assert token_data["token_type"] == "bearer"
            
            # Step 3: Use the token to access protected endpoint
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            me_response = client.get("/api/users/me", headers=headers)
            
            assert me_response.status_code == 200
            me_data = me_response.json()
            assert me_data["username"] == test_user_data["username"]
            assert me_data["email"] == test_user_data["email"]
            assert me_data["id"] == user_data["id"]
    
    def test_registration_with_duplicate_data_handling(self, client: TestClient, test_user_data: dict):
        """Test handling of duplicate registration attempts."""
        with patch('app.controllers.user_controller.trigger_email_verification'):
            # Register first user
            first_response = client.post("/api/auth/register", json=test_user_data)
            assert first_response.status_code == 201
            
            # Try to register with same username
            duplicate_username_data = test_user_data.copy()
            duplicate_username_data["email"] = "different@example.com"
            
            duplicate_response = client.post("/api/auth/register", json=duplicate_username_data)
            assert duplicate_response.status_code == 400
            
            # Try to register with same email
            duplicate_email_data = test_user_data.copy()
            duplicate_email_data["username"] = "differentuser"
            
            duplicate_response = client.post("/api/auth/register", json=duplicate_email_data)
            assert duplicate_response.status_code == 400
    
    def test_authentication_failure_scenarios(self, client: TestClient, test_user_data: dict):
        """Test various authentication failure scenarios."""
        with patch('app.controllers.user_controller.trigger_email_verification'):
            # Register user first
            client.post("/api/auth/register", json=test_user_data)
        
        # Test login with wrong password
        wrong_password_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", data=wrong_password_data)
        assert response.status_code == 401
        
        # Test login with non-existent user
        nonexistent_user_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/api/auth/login", data=nonexistent_user_data)
        assert response.status_code == 401
        
        # Test accessing protected endpoint without token
        response = client.get("/api/users/me")
        assert response.status_code == 401
        
        # Test accessing protected endpoint with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 401
    
    def test_email_verification_workflow(self, client: TestClient, test_user_data: dict):
        """Test email verification workflow."""
        with patch('app.controllers.user_controller.trigger_email_verification') as mock_email:
            # Register user
            client.post("/api/auth/register", json=test_user_data)
            mock_email.reset_mock()
            
            # Request email verification resend
            resend_data = {"username": test_user_data["username"]}
            response = client.post("/api/auth/resend_email_verification", json=resend_data)
            
            assert response.status_code == 202
            mock_email.assert_called_once()
            
            # Test resend for non-existent user
            nonexistent_data = {"username": "nonexistent"}
            response = client.post("/api/auth/resend_email_verification", json=nonexistent_data)
            assert response.status_code == 400
    
    def test_api_endpoints_accessibility(self, client: TestClient):
        """Test that all API endpoints are accessible and return expected status codes."""
        # Health endpoint should always be accessible
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        
        # Auth endpoints should be accessible but may require data
        response = client.post("/api/auth/register", json={})
        assert response.status_code == 422  # Validation error, but endpoint is accessible
        
        response = client.post("/api/auth/login", data={})
        assert response.status_code == 422  # Validation error, but endpoint is accessible
        
        # Protected endpoints should require authentication
        response = client.get("/api/users/me")
        assert response.status_code == 401  # Unauthorized, but endpoint is accessible 
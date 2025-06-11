import pytest
from datetime import datetime
from uuid import UUID
from pydantic import ValidationError

from app.models.users import (
    User, UserCreate, UserRead, UserRegistrationParameters, 
    EmailVerificationParameters
)
from app.models.auth import Token


class TestUserModels:
    """Test user-related models."""
    
    def test_user_model_creation(self):
        """Test creating a User model instance."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "hashed_password": "hashed_password_here",
            "is_active": True,
            "verified_email": False
        }
        
        user = User(**user_data)
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"
        assert user.hashed_password == "hashed_password_here"
        assert user.is_active is True
        assert user.verified_email is False
        assert isinstance(user.id, UUID)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
    
    def test_user_model_defaults(self):
        """Test User model default values."""
        minimal_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "hashed_password": "hashed_password_here"
        }
        
        user = User(**minimal_data)
        
        assert user.is_active is True  # Default value
        assert user.verified_email is False  # Default value
        assert user.id is not None  # Auto-generated
        assert user.created_at is not None  # Auto-generated
        assert user.updated_at is not None  # Auto-generated
    
    def test_user_create_model(self):
        """Test UserCreate model."""
        user_create_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "plaintext_password",
            "is_active": True
        }
        
        user_create = UserCreate(**user_create_data)
        
        assert user_create.email == "test@example.com"
        assert user_create.username == "testuser"
        assert user_create.full_name == "Test User"
        assert user_create.password == "plaintext_password"
        assert user_create.is_active is True
    
    def test_user_read_model(self):
        """Test UserRead model."""
        user_read_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "is_active": True,
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now()
        }
        
        user_read = UserRead(**user_read_data)
        
        assert user_read.email == "test@example.com"
        assert user_read.username == "testuser"
        assert user_read.full_name == "Test User"
        assert user_read.is_active is True
        assert user_read.id == "123e4567-e89b-12d3-a456-426614174000"
        assert isinstance(user_read.created_at, datetime)
    
    def test_user_registration_parameters(self):
        """Test UserRegistrationParameters model."""
        registration_data = {
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User",
            "email": "test@example.com"
        }
        
        params = UserRegistrationParameters(**registration_data)
        
        assert params.username == "testuser"
        assert params.password == "password123"
        assert params.full_name == "Test User"
        assert params.email == "test@example.com"
    
    def test_user_registration_parameters_invalid_email(self):
        """Test UserRegistrationParameters with invalid email."""
        registration_data = {
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User",
            "email": "invalid-email"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UserRegistrationParameters(**registration_data)
        
        assert "email" in str(exc_info.value)
    
    def test_user_registration_parameters_optional_full_name(self):
        """Test UserRegistrationParameters with optional full_name."""
        registration_data = {
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com"
            # full_name is optional and defaults to None
        }
        
        params = UserRegistrationParameters(**registration_data)
        
        assert params.username == "testuser"
        assert params.password == "password123"
        assert params.email == "test@example.com"
        assert params.full_name is None
    
    def test_email_verification_parameters(self):
        """Test EmailVerificationParameters model."""
        verification_data = {
            "username": "testuser"
        }
        
        params = EmailVerificationParameters(**verification_data)
        
        assert params.username == "testuser"
    
    def test_email_verification_parameters_missing_username(self):
        """Test EmailVerificationParameters with missing username."""
        with pytest.raises(ValidationError) as exc_info:
            EmailVerificationParameters()
        
        assert "username" in str(exc_info.value)


class TestAuthModels:
    """Test authentication-related models."""
    
    def test_token_model(self):
        """Test Token model."""
        token_data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        
        token = Token(**token_data)
        
        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert token.token_type == "bearer"
    
    def test_token_model_missing_fields(self):
        """Test Token model with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            Token(access_token="token_here")  # Missing token_type
        
        assert "token_type" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            Token(token_type="bearer")  # Missing access_token
        
        assert "access_token" in str(exc_info.value) 
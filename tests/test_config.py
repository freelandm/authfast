import pytest
import os
from unittest.mock import patch

from app.config import Settings, settings


class TestConfiguration:
    """Test application configuration."""
    
    def test_settings_default_values(self):
        """Test that settings have expected default values."""
        test_settings = Settings()
        
        # Test default database URL
        assert test_settings.DATABASE_URL == "postgresql://matt:bigdog@db:5432/app"
        assert test_settings.LOCAL_DATABASE_URL == "postgresql://matt:bigdog@localhost:5432/app"
    
    def test_settings_from_environment(self):
        """Test that settings can be loaded from environment variables."""
        env_vars = {
            'DATABASE_URL': 'postgresql://testuser:testpass@testhost:5432/testdb',
            'ADMIN_EMAIL': 'test@example.com',
            'ADMIN_USERNAME': 'testadmin',
            'ADMIN_FULL_NAME': 'Test Admin',
            'ADMIN_PASSWORD': 'testpassword',
            'ADMIN_HASHED_PASSWORD': 'hashed_test_password',
            'SENDGRID_API_KEY': 'test_sendgrid_key',
            'APPLICATION_HOSTNAME': 'http://test.example.com',
            'JWT_SECRET_KEY': 'test_jwt_secret'
        }
        
        with patch.dict(os.environ, env_vars):
            test_settings = Settings()
            
            assert test_settings.DATABASE_URL == 'postgresql://testuser:testpass@testhost:5432/testdb'
            assert test_settings.ADMIN_EMAIL == 'test@example.com'
            assert test_settings.ADMIN_USERNAME == 'testadmin'
            assert test_settings.ADMIN_FULL_NAME == 'Test Admin'
            assert test_settings.ADMIN_PASSWORD == 'testpassword'
            assert test_settings.ADMIN_HASHED_PASSWORD == 'hashed_test_password'
            assert test_settings.SENDGRID_API_KEY == 'test_sendgrid_key'
            assert test_settings.APPLICATION_HOSTNAME == 'http://test.example.com'
            assert test_settings.JWT_SECRET_KEY == 'test_jwt_secret'
    
    def test_settings_required_fields(self):
        """Test that required settings fields are defined."""
        # These fields should be required and will raise ValidationError if not provided
        required_fields = [
            'ADMIN_EMAIL',
            'ADMIN_USERNAME', 
            'ADMIN_FULL_NAME',
            'ADMIN_PASSWORD',
            'ADMIN_HASHED_PASSWORD',
            'SENDGRID_API_KEY',
            'APPLICATION_HOSTNAME',
            'JWT_SECRET_KEY'
        ]
        
        for field in required_fields:
            assert hasattr(Settings, field), f"Required field {field} not found in Settings"
    
    def test_global_settings_instance(self):
        """Test that the global settings instance is properly initialized."""
        assert settings is not None
        assert isinstance(settings, Settings)
        
        # Test that we can access settings attributes
        assert hasattr(settings, 'DATABASE_URL')
        assert hasattr(settings, 'LOCAL_DATABASE_URL')
    
    def test_settings_config_class(self):
        """Test that Settings has proper configuration."""
        assert hasattr(Settings, 'Config')
        assert hasattr(Settings.Config, 'env_file')
        assert Settings.Config.env_file == ".env" 
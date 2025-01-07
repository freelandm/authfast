from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://matt:bigdog@db:5432/app"
    LOCAL_DATABASE_URL: str = "postgresql://matt:bigdog@localhost:5432/app"
    ADMIN_EMAIL: str
    ADMIN_USERNAME: str
    ADMIN_FULL_NAME: str
    ADMIN_PASSWORD: str
    ADMIN_HASHED_PASSWORD: str
    SENDGRID_API_KEY: str
    APPLICATION_HOSTNAME: str
    JWT_SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
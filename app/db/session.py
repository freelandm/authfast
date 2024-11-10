from sqlmodel import create_engine, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_session_generator():
    with Session(engine) as session:
        yield session

def get_session():
    return next(get_session_generator())
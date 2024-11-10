from inflect import engine as inflect_engine
from sqlmodel import SQLModel

inflect = inflect_engine()

class BaseSQLModel(SQLModel):
    """
        Base model for all database models
        Overrides singular table names with plural name
    """
    @classmethod
    @property
    def __tablename__(cls) -> str:
        return inflect.plural(cls.__name__.lower())
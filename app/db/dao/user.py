from sqlmodel import select, update
from app.db.session import get_session

from app.models.users import User

class UserDao:
    def create_one(self, user: User) -> User:
        session = get_session()
        session.add(user)
        session.commit()
        return self.get_one_by_username(username=user.username)

    def get_one_by_id(self, id: str) -> User:
        session = get_session()
        statement = select(User).where(User.id == id).limit(1)
        results = session.exec(statement)
        return results.first()

    def get_one_by_username(self, username: str) -> User:
        session = get_session()
        statement = select(User).where(User.username == username).limit(1)
        results = session.exec(statement)
        return results.first()

    def get_one_by_email_address(self, email_address: str) -> User:
        session = get_session()
        statement = select(User).where(User.email == email_address).limit(1)
        results = session.exec(statement)
        return results.first()

    def mark_email_address_verified(self, email_address: str) -> User:
        # first, mark user email address as verified
        session = get_session()
        statement = update(User).where(User.email == email_address).values(verified_email=True)
        session.exec(statement)
        session.commit()
        # then, return the user from the database
        return self.get_one_by_email_address(email_address=email_address)


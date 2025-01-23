from app.db.session import engine
from app.models import User
from sqlmodel import select, insert, Session
from app.config import settings
import logging
import os

def inject_admin_user():
    email=os.environ.get('ADMIN_EMAIL')
    uname=os.environ.get('ADMIN_USERNAME'),
    name=os.environ.get('ADMIN_FULL_NAME'),
    hash_pass=os.environ.get('ADMIN_HASHED_PASSWORD'),
    logging.info(f'{email=} {uname=} {name=} {hash_pass}')
    try:
        with Session(engine) as session:
            admin = User(
                email=email,
                username=uname,
                is_active=True,
                full_name=name,
                hashed_password=hash_pass
            )
            session.add(admin)
            session.commit()
    except Exception as e:
        logging.warning(f'Failed to create admin user for {email}: {e}')

# bootstraps the application with configurable admin user
def bootstrap():
    inject_admin_user()
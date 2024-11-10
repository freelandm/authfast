import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends,  HTTPException, status
from app.db.dao import user_dao
from app.models.users import User

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import logging
from app.logger import logger
import os

# https://github.com/pyca/bcrypt/issues/684
# suppresses error
# passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
# AttributeError: module 'bcrypt' has no attribute '__about__'
logging.getLogger('passlib').setLevel(logging.ERROR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY via 'openssl rand -hex 32'
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", {}).get("username")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = user_dao.get_one_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
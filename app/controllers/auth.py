
from dataclasses import dataclass
from app.db.dao import UserDao
from app.dependencies.auth import SECRET_KEY, ALGORITHM

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from app.db.dao import user_dao

@dataclass
class AuthController:
    user_dao: UserDao

    def verify_email(
            self,
            token: str
        ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email_address: str = payload.get("sub", {}).get("email_address_verification")
            if email_address is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = user_dao.mark_email_address_verified(email_address=email_address)
        if user is None:
            raise credentials_exception
        return user

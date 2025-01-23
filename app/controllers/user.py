from dataclasses import dataclass
import os
from app.controllers.email import EmailController
from app.db.dao import UserDao
from app.dependencies.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context

import jwt
from typing import Union
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.models.users import User, UserRegistrationParameters
from app.params import SendEmailParams


@dataclass
class UserController:
    user_dao: UserDao
    email_controller: EmailController

    def register(self, params: UserRegistrationParameters) -> User:
        # create user in database
        existing_user = self.user_dao.get_one_by_username(params.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"username {params.username} already taken"
            )
        existing_user = self.user_dao.get_one_by_email_address(params.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"user with email {params.username} already exists"
            )
        user = User(
            email=params.email,
            username=params.username,
            hashed_password=self.get_password_hash(params.password),
            full_name=params.full_name
        )
        return self.user_dao.create_one(
            user=user
        )
    
    def trigger_email_verification(self, user: User):
        verification_link = self.generate_email_verification_link(user=user)
        application_hostname = os.environ.get("APPLICATION_HOSTNAME")
        return self.email_controller.send_email(
            params=SendEmailParams(
                to=user.email,
                subject=f'Email verification for {application_hostname}',
                content=f'{verification_link}'
                #content=f'''
                #    Please click the <a href="">link</a> to verify your email address for {application_hostname}
                #''',
            )
        )
    
    def generate_email_verification_link(self, user: User) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self.create_token(
            data={"sub": {"email_address_verification": user.email}}, expires_delta=access_token_expires
        )
        application_hostname = os.environ.get('APPLICATION_HOSTNAME')
        return f'{application_hostname}/api/auth/verify_email?token={token}'
    
    def authenticate(self, username: str, password: str) -> str:
        user: User = self.user_dao.get_one_by_username(username=username)
        valid_user = user and self.verify_password(password, user.hashed_password)
        if not valid_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.verified_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your email address",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    def generate_access_token_for_user(self, user: User):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_token(
            data={"sub": {"username": user.username}}, expires_delta=access_token_expires
        )
        return access_token

    def create_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        if not expires_delta:
            expires_delta = timedelta(minutes=15)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
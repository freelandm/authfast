from typing import Annotated
from fastapi import APIRouter, Depends
from models.users import User
from dependencies.auth import get_current_active_user

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

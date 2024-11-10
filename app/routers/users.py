from typing import Annotated
from fastapi import APIRouter, Depends
from app.models.users import User
from app.dependencies.auth import get_current_active_user

router = APIRouter()


@router.get("/api/users/me", tags=["users"])
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user

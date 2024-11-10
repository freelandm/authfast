from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.auth import Token
from app.controllers import user_controller, auth_controller
from app.models.users import UserRead, UserRegistrationParameters, EmailVerificationParameters

router = APIRouter(prefix="/api/auth")

@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = user_controller.authenticate(username=form_data.username, password=form_data.password)
    return Token(
        access_token=user_controller.generate_access_token_for_user(user=user),
        token_type="bearer"
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    params: UserRegistrationParameters,
) -> UserRead:
    user = user_controller.register(params=params)
    user_controller.trigger_email_verification(user=user)
    return user

@router.post("/resend_email_verification", status_code=status.HTTP_202_ACCEPTED)
async def resend_email_verification(params: EmailVerificationParameters):
    user = user_controller.user_dao.get_one_by_username(username=params.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {params.username} not found"
        )
    if user.verified_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user_controller.trigger_email_verification(user=user)

@router.get("/verify_email")
async def verify_email(
    token: str
):
    return auth_controller.verify_email(token=token)
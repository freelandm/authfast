from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_active_user
from app.controllers import email_controller

from app.params import SendEmailParams

router = APIRouter(prefix="/api/email")

@router.post("", dependencies=[Depends(get_current_active_user)])
async def send_email_to(params: SendEmailParams):
    return email_controller.send_email(
        params=params
    )
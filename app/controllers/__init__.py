from app.controllers.auth import AuthController
from app.controllers.user import UserController
from app.controllers.email import EmailController
from app.db.dao import user_dao
from sendgrid import SendGridAPIClient
import os

email_controller = EmailController(
    client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
)

user_controller = UserController(
    user_dao=user_dao,
    email_controller=email_controller
)

auth_controller = AuthController(
    user_dao=user_dao
)
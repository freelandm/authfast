from pydantic import BaseModel, EmailStr

class SendEmailParams(BaseModel):
    subject: str = "Incoming email"
    content: str = "Check out how cool I am, I can integrate with 3rd party systems"
    to: EmailStr
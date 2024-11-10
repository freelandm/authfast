from app.params import SendEmailParams

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dataclasses import dataclass
import os

@dataclass
class EmailController:
    client: SendGridAPIClient
    from_email: str = os.environ.get('ADMIN_EMAIL')

    def send_email(self, params: SendEmailParams):
        # using SendGrid's Python Library
        # https://github.com/sendgrid/sendgrid-python
        message = Mail(
            from_email=self.from_email,
            to_emails=params.to,
            subject=params.subject,
            html_content=params.content)
        return self.client.send(message)
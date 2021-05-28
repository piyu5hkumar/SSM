from typing import Tuple
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    Content,
)
from django.conf import settings
import os


class SendGrid:
    SENDGRID_USE = settings.SENDGRID_USE
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
    SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "")
    SENDGRID_SENDER_EMAIL = os.environ.get("SENDGRID_SENDER_EMAIL", "")

    def __init__(self) -> None:

        """
        This is the constructor for SendGrid class.
        In future a logger will also be initialized here.
        """

        if self.SENDGRID_USE:
            self.sendgrid_client = SendGridAPIClient(self.SENDGRID_API_KEY)

    def mail_object(self, to_email: str, verification_link: str) -> Mail:

        """
        This method will create a Mail object which will be sent by the email,
        Mail object consists of from_email, to_emails, subject, template_id and dynamic_template_data
        """

        mail = Mail(
            from_email=self.SENDGRID_SENDER_EMAIL,
            to_emails=to_email,
            subject="SSM Forgot Password hero",
        )
        mail.template_id = self.SENDGRID_TEMPLATE_ID
        mail.dynamic_template_data = {"verification_link": verification_link}

        return mail

    def send_email(self, to_email: str, verification_link: str) -> Tuple[bool, str]:

        """
        This method will send the mail and returns a tuple of bool and str,
        corresponding to success and success message or error and error message(in case of failure)
        """

        if not self.SENDGRID_USE:
            return True, "Mail was not sent because sendgrid use is set to false"
        try:
            mail = self.mail_object(to_email, verification_link)
            sendgrid_response = self.sendgrid_client.send(mail)
            return True, str(sendgrid_response.headers)
        except Exception as e:
            return False, str(e)

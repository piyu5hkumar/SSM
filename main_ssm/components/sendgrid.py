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

import os


class SendGrid:
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    sendgrid_template_id = os.environ.get("SENDGRID_TEMPLATE_ID")
    sendgrid_sender_email = os.environ.get("SENDGRID_SENDER_EMAIL")
    use_sendgrid = os.environ.get("SENDGRID_USE")

    def __init__(self) -> None:

        """
        This is the constructor for SendGrid class.
        In future a logger will also be initialized here.
        """

        if self.use_sendgrid:
            self.sendgrid_client = SendGridAPIClient(self.sendgrid_api_key)

    def get_mail_object(self, to_email: str, verification_link: str) -> Mail:

        """
        This method will create a Mail object which will be sent by the email,
        Mail object consists of from_email, to_emails, subject, template_id and dynamic_template_data
        """

        message = Mail(
            from_email=self.sendgrid_sender_email,
            to_emails=to_email,
            subject="SSM Forgot Password hero",
        )
        message.template_id = self.sendgrid_template_id
        message.dynamic_template_data = {"verification_link"}

        return message

    def send_email(self, to_email: str, verification_link: str) -> Tuple[bool, str]:

        """
        This method will send the mail and returns a tuple of bool and str,
        corresponding to success and success message or error and error message(in case of failure)
        """

        try:
            mail = self.get_mail_object(to_email, verification_link)
            sendgrid_response = self.sendgrid_client.send(mail)
            return True, str(sendgrid_response.headers)
        except Exception as e:
            False, str(e)

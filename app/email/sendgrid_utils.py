import os

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send_welcome(user_email):
    """
    Sends a welcome email to the user via
    SendGrid V3 API.

    TODO: Create Templates for Emails
    TODO: Remove Generic Except

    :param user_email: User to send email
    """
    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    from_email = Email(current_app.config["SENDGRID_DEFAULT_FROM"])
    to_email = To(user_email)
    subject = "Welcome to Climate Mind!"
    content = Content(
        "text/plain",
        "You have successfully registered for Climate Mind.\nPlease do not reply to this email.\n",
    )
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg.send(mail)

    except Exception as e:
        print(e.message)

from email import message
import os

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.sendgrid.templates.welcome_email import WELCOME_EMAIL


def send_welcome_email(user_email, user_first_name):
    """
    Sends a welcome email to the user after registering via the SendGrid API.

    Parameters
    =====================
    user_email - The email used to register an account.
    user_first_name - The user's first name.

    """
    sg, from_email = set_up_sendgrid()

    to_email = To(
        email=user_email,
        substitutions={
            "-user_first_name-": user_first_name,
            "-user_email-": user_email,
        },
    )
    subject = "Welcome to Climate Mind!"
    content = Content("text/html", WELCOME_EMAIL)
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg.send(mail)
    except Exception as e:
        print(e)


def set_up_sendgrid():
    """
    Initial setup to use the SendGrid API. Creates the client, and sets the default email address to send emails from.
    """

    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    from_email = Email(current_app.config["SENDGRID_DEFAULT_FROM"])

    return sg, from_email

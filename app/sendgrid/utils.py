from flask import current_app
from python_http_client import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from app import db
from app.models import Conversations, Users
from app.sendgrid.templates.reset_password import RESET_PASSWORD_EMAIL
from app.sendgrid.templates.user_b_shared_email import USER_B_SHARED_EMAIL
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
            "-preview_text-": f"Welcome aboard, {user_first_name}! We just wanted to say thank you for signing up to use our app. Climate Mind is an app which helps people start meaningful conversations about climate change.",
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


def send_user_b_shared_email(conversation_uuid):
    """
    Gets user a's first name, user b's name and user a's email from the database.
    Sends a confirmation email to user a when user b has consented to share to let them know that they can start their conversation.

    Parameters
    =====================
    conversation_uuid - (UUID) the unique id for the conversation

    """

    # currently allowing the db interaction to fail silently to not block the consent endpoint from returning its response if something goes wrong with the email building
    try:
        user_a_first_name, user_b_name, user_a_email = (
            db.session.query(
                Users.first_name, Conversations.receiver_name, Users.user_email
            )
            .join(
                Users,
                Users.user_uuid == Conversations.sender_user_uuid,
            )
            .filter(Conversations.conversation_uuid == conversation_uuid)
            .one_or_none()
        )
    except:
        print("Something went wrong while retrieving information from the db.")

    sg, from_email = set_up_sendgrid()

    to_email = To(
        email=user_a_email,
        substitutions={
            "-preview_text-": f"How exciting, {user_a_first_name}! Your friend, {user_b_name} has taken the Climate Mind quiz and has some conversation starters to share with you.",
            "-user_a_first_name-": user_a_first_name,
            "-user_b_name-": user_b_name,
            "-conversation_uuid-": str(conversation_uuid),
        },
    )
    subject = f"Ready for a climate conversation with {user_b_name}?"
    content = Content("text/html", USER_B_SHARED_EMAIL)
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg.send(mail)
    except Exception as e:
        print(e)


def send_reset_password_email(
    user_email: str, reset_url: str, expire_hours: int
) -> None:
    """
    Sends a reset password URL to the user via the SendGrid API.

    Parameters
    =====================
    user_email - The email used to register an account.

    """
    sg, from_email = set_up_sendgrid()

    to_email = To(
        email=user_email,
        substitutions={
            "-preview_text-": "Here is a link to reset your password for Climate Mind",
            "-reset_link-": reset_url,
            "-reset_password_expire_hours-": str(expire_hours),
        },
    )
    subject = "Reset your Climate Mind password!"
    text_version = (
        "Here is a link to reset your password for Climate Mind "
        f"{reset_url} Please be advised, that the provided link will "
        f"expire in 3 hours. If you didn't request this please email "
        f"us to let us know hello@climatemind.org"
    )

    text_content = Content("text/plain", text_version)
    html_content = Content("text/html", RESET_PASSWORD_EMAIL)
    mail = Mail(from_email, to_email, subject, text_content, html_content=html_content)

    try:
        sg.send(mail)
    except HTTPError as e:
        current_app.logger.exception(
            "Unable to send reset password email", extra={"error": e.to_dict}
        )
        current_app.logger.debug(e.to_dict)
    except:
        current_app.logger.exception("Unable to send reset password email")


def set_up_sendgrid():
    """
    Initial setup to use the SendGrid API. Creates the client, and sets the default email address to send emails from.
    """

    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    from_email = Email(current_app.config["SENDGRID_DEFAULT_FROM"])

    return sg, from_email

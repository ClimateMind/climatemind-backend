from app import db
import os
from pathlib import Path
import sys
from app import create_app
from app.models import Users
from sqlalchemy.exc import SQLAlchemyError

# Determine the root path of the project
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent
sys.path.append(str(project_root))

print(f"The root path of the app is: {project_root}")

# Initialize the Flask app
app = create_app()

# Import db after creating the app


def delete_user_by_email(email):
    """
    Deletes a user account based on the provided email.
    """
    with app.app_context():
        try:
            if not email:
                print("Email must be provided.")
                return

            # Find the user by the provided email
            user = Users.query.filter_by(user_email=email).one_or_none()

            if not user:
                print("User with this email does not exist.")
                return

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            print("User account successfully deleted.")

        except SQLAlchemyError as e:
            # Roll back the session and changes to the db if an error occurs while deleting the user
            db.session.rollback()
            print("An error occurred while deleting user from the database:", str(e))

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    email_to_delete = input("Enter the email of the user to delete: ")
    delete_user_by_email(email_to_delete)

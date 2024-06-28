import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def configure_google_oauth(app):
    oauth.init_app(app)
    google = oauth.register(
        'google',
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://www.googleapis.com/oauth2/v4/token',
        redirect_uri='http://localhost:5000/login/callback',
        client_kwargs={'scope': 'openid profile email'},
    )
    return google

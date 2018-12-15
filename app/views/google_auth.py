from google_auth_oauthlib.helpers import session_from_client_secrets_file
from google_auth_oauthlib.flow import Flow
from google.auth.jwt import decode
from requests_oauthlib import OAuth2Session
from flask import session, redirect, request, Flask, url_for
from flask.views import MethodView
from flask_login import login_user
from app.services import UserService
from app.models import User, OpenIdAccount

class GoogleAuthConfig():
    def __init__(self, secrets_file, user_service: UserService):
        self.user_service = user_service
        # Verify the secrets_file is in the correct format and save the parsed configuration
        self.scopes = ['email', 'openid']
        session, config = session_from_client_secrets_file(secrets_file, scopes = self.scopes)
        self.config = config
        self.redirect_uri = config['web']['redirect_uris'][0]

    def build_flow(self, state = None):
        flow = Flow.from_client_config(
            self.config,
            scopes = self.scopes,
            redirect_uri = self.redirect_uri,
            state = state)
        return flow

class GoogleLoginView(MethodView):
    def __init__(self, google_auth: GoogleAuthConfig):
        self.google_auth = google_auth

    def get(self):
        # Build the url to redirect the user to for google authentication
        flow = self.google_auth.build_flow()
        auth_url, state = flow.authorization_url()

        # State is used to prevent CSRF, keep this for later.
        session['oauth_state'] = state

        # Redirect the user to the google authentication url
        return redirect(auth_url)

class GoogleAuthCallback(MethodView):
    def __init__(self, google_auth: GoogleAuthConfig):
        self.google_auth = google_auth

    ## The function that will be redirected to by the google authentication servers
    def get(self):
        # Rebuild the flow from the original request using the state stored in the session
        flow = self.google_auth.build_flow(state = session['oauth_state'])
        
        # Exchange the received one time authorization code for an OpenId token
        token = flow.fetch_token(authorization_response = request.url)

        # Decode the id_token to capture user information
        id_token = token['id_token']
        user_claims = decode(id_token, verify = False)

        # Get or add a user account associated with this google account
        user = self.google_auth.user_service.get_or_add_openid_account(
            issuer_identifier = user_claims['iss'],
            subject_identifier = user_claims['sub'])
        
        # Let the Flask-Login extension know about the user
        login_user(user)

        #Redirect the user to the home page
        return redirect(url_for('categories_view'))

def add_routes(app: Flask, google_auth: GoogleAuthConfig):
    # Register the google authentication callback url with the application
    # The URL is pre-registered with google and is tied to this application's client_id.
    # We'll use the GoogleAuthCallback class as a view that google can redirect to.
    app.add_url_rule(
        '/oauth2callback', 
        view_func = GoogleAuthCallback.as_view('google_callback', google_auth = google_auth))
    app.add_url_rule(
        '/login',
        view_func = GoogleLoginView.as_view('google_login_view', google_auth = google_auth))
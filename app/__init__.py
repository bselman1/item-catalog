from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from .services import CatalogService, UserService
from .models import DbSetup
from .views import init_app as views_init_app, GoogleAuthConfig
import os

def create_app(config_file_path: str):
    app = Flask(__name__)

    ## Load the application configuration 
    app.config.from_pyfile(config_file_path)
    
    ## Set up cross site forgery protection that WTForms uses 
    csrf = CSRFProtect(app)
    csrf.init_app(app)

    ## Set up the DbSetup object to connect to the database 
    db_setup = DbSetup(app.config['DATABASE_URI'])
    db_setup.initialize_database()

    ## Build services that the application will use 
    catalog_service = CatalogService(db_setup)
    user_service = UserService(db_setup)

    ## Set up the Flask Login Manager
    login_manager = LoginManager()
    login_manager.user_loader(user_service.get_user)
    login_manager.init_app(app)
    
    ## Set up the google authentication configuration
    google_config = GoogleAuthConfig(app.config['GOOGLE_SECRETS_FILE'], user_service)

    ## Control wheter or not OAuth will allow non https transport
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config['OAUTHLIB_INSECURE_TRANSPORT']
    
    ## Controls how strict the matching of scopes returned by the OAuth server against the requested scopes is
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = app.config['OAUTHLIB_RELAX_TOKEN_SCOPE']
    
    ## Inject the required services into the views used by the application 
    views_init_app(app, catalog_service, google_config)

    ## Return the configured application 
    return app
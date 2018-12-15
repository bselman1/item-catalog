# Item-Catalog
## Installation
- Clone this repository to your local computer
- Open a terminal window and cd to the cloned repository
- Create a python virtual environment:
```
    python -m venv venv
```
- Install the required packages:
```
    pip install -r requirements.txt
```

## Configuration
There is a default configuration file 'default_config.py' that will allow the application to run by default but should be updated with values appropriate to your environment.
```
DEBUG = True
FLASK_ENV =  'development'
SECRET_KEY = 'MUST_OVERRIDE'
DATABASE_URI = 'sqlite:///item_catalog.db'
GOOGLE_SECRETS_FILE = './google_secrets.json'
OAUTHLIB_INSECURE_TRANSPORT = '1'
OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
```

- DEBUG should be changed to False in a production environment
- FLASK_ENV should be changed to production in a production environment
- SECRET_KEY should be overrided with a secure value
- OAUTHLIB_INSECURE_TRANSPORT should be removed if this application is run in an HTTPS environment

Normaly the google_secrets.json file wouldn't be included in a git repository as it contains the secret key that this application uses to communicate with the Google authentication servers. It's included here for this demo so that it will run and allow Google OpenId login.

## Running the application
- Open a terminal window with the item-catalog project as the working directory.
- Set the FLASK_APP environment variable
```
   SET FLASK_APP=run.py
```
- Activate the python virtual environment
```
   venv\scripts\activate.bat
```
- Run the development server
```
   python -m flask run --no-debugger --no-reload --port 5005
```
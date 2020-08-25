from flask import Flask
from config import Config
# by installing extensions (I see they are actually wrappers in some cases) they can also install incompatible by
# default components like SQLAlchemy, the same name they have inside extension so instead of importing them directly
# we are importing them by extensions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask_login is the extension adding functionality of remembering user even by closing the browser window
from flask_login import LoginManager

# __name__ is something like a mode of flask application that is default and works good on basic projects
app = Flask(__name__)
# importing flask settings from specific object (class) to keep config.py and __init__.py separate files
app.config.from_object(Config)
# we also need instances for database and migrate tool for it since it works based on instances
# instance of something is a place in the memory and software so it can work along an application
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# flask-login needs to have an instance like some others flask extensions
login = LoginManager(app)

# routes will need the app variable, to prevent looping (circular imports) we put it after the app variable (object)
# models will be used to define the structure of the database
from app import routes, models

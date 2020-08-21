from flask import Flask
from config import Config

# __name__ is something like a mode of flask application that is default and works good on basic projects
app = Flask(__name__)
# importing flask settings from specific object (class) to keep config.py and __init__.py separate files
app.config.from_object(Config)

# routes will need the app variable, to prevent looping (circular imports) we put it after the app variable (object)
from app import routes

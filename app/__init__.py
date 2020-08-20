from flask import Flask

# __name__ is something like a mode of flask application that is default and works good on basic projects
app = Flask(__name__)

# routes will need the app variable, to prevent looping (circular imports) we put it after the app variable (object)
from app import routes

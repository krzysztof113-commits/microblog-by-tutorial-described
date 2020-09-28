from flask import Blueprint

# The Blueprint class takes the name of the blueprint,
# the name of the base module (typically set to __name__).
bp = Blueprint('errors', __name__)

from app.errors import handlers

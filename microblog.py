# this is a top-level python script that defines the application instance/case
# the statement imports the app variable that is a member of the app package
from app import app, db
from app.models import User, Post
from app import cli

# To start the server, we need to tell flask where is this python script by
# using 'set FLASK_APP=microblog.py' in a terminal (set = export for linux)
# then just 'flask run' in a terminal.

# Environment variables are not remembered across terminal sessions.
# To make it easier, flask has python support of environment variables
# that automatically import on 'flask run'.
# You just need to use 'pip install python-dotenv' before.


# This decorator runs after 'flask shell' from terminal,
# the improved python console which understands flask better.
@app.shell_context_processor
def make_shell_context():
    # It needs to be dictionary because every key needs to have a name
    # (an alias) that will be used by shell.
    # Then you can work with database entities without importing them,
    # they are being imported here above instead.
    return {'db': db, 'User': User, 'Post': Post}

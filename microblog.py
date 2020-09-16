# this is a top-level python script that defines the application instance/case
# the statement imports the app variable that is a member of the app package
from app import app, db
from app.models import User, Post
from app import cli

# to actually start the server we need to tell flask where is this python script
# by using 'set FLASK_APP=microblog.py' in a terminal (set = export for linux)
# then just 'flask run' in a terminal

# environment variables are not remembered across terminal sessions
# to make it easier flask has python support of environment variables that automatically import on 'flask run'
# you just need to 'pip install python-dotenv', before we just installed our 'flask' (you can see requirements.txt now)


# this decorator runs after 'flask shell' from terminal, the improved python console which understands flask better
@app.shell_context_processor
def make_shell_context():
	# it needs to be dictionary because every key needs to have a name (an alias) that will be used by shell
	# then you can work with database entities without importing them, they are being imported here above instead
	return {'db': db, 'User': User, 'Post': Post}

from flask import Flask
from config import Config
# by installing extensions (I see they are actually wrappers in some cases) they can also install incompatible by
# default components like SQLAlchemy, the same name they have inside extension so instead of importing them directly
# we are importing them by extensions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask_login is the extension adding functionality of remembering user even by closing the browser window
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

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
# this flask_login feature sets the name of which view function redirect to if the page is restricted by @login_required
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# routes will need the app variable, to prevent looping (circular imports) we put it after the app variable (object)
# models will be used to define the structure of the database
from app import routes, models, errors

if not app.debug:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			# if we about to set tuple then we know which value and orders it needs to have, it should not be added etc.
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)
		# fake SMTP email server is run by: python -m smtpd -n -c DebuggingServer localhost:8025
		# then: set MAIL_SERVER=localhost, and: set MAIL_PORT=8025, where: FLASK_DEBUG must be 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	# there is general setting for app.logger to which errors to capture (we are lowering the level, also in above)
	# they are DEBUG, INFO, WARNING, ERROR and CRITICAL in increasing order of severity
	app.logger.setLevel(logging.INFO)
	# As a first interesting use of the log file, the server writes a line to the logs each time it starts.
	# When this application runs on a production server, these log entries will tell you when the server was restarted.
	app.logger.info('Microblog startup')

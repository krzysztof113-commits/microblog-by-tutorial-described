from flask import Flask
from config import Config
# By installing extensions (I see they are actually wrappers in some cases)
# they can also install incompatible by default components like SQLAlchemy,
# the same name they have inside extension so instead of
# importing them directly, we are importing them by extensions.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask_login is the extension adding functionality of remembering user,
# even by closing the browser window.
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
# request thing can load custom things on each request
from flask import request, current_app
from flask_babel import lazy_gettext as _l

# __name__ is something like a mode of flask application that is default
# and works good on basic projects
# importing flask settings from specific object (class) to keep config.py
# We also need instances for database and migrate tool for it
# since it works based on instances. Instance of something is a place
# in the memory and software so it can work along an application.
db = SQLAlchemy()
migrate = Migrate()
# flask-login needs to have an instance like some others flask extensions.
login = LoginManager()
# This flask_login feature sets the name of which view function redirect to
# if the page is restricted by @login_required.
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (
                    app.config['MAIL_USERNAME'],
                    app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                # If we about to set tuple then we know which value and
                # orders it needs to have, it should not be added etc.
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            # The fake SMTP email server is run by:
            # python -m smtpd -n -c DebuggingServer localhost:8025
            # then: set MAIL_SERVER=localhost, and: set MAIL_PORT=8025,
            # where: FLASK_DEBUG must be 0.
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        # There is general setting for app.logger to which errors to capture
        # (we are lowering the level, also in above). (min. to max. info).
        # They are DEBUG, INFO, WARNING, ERROR and CRITICAL ^
        app.logger.setLevel(logging.INFO)
        # The server writes a line to the logs each time it starts.
        # When this application runs on a production server,
        # these log entries will tell you when the server was restarted.
        app.logger.info('Microblog startup')

    return(app)


# routes will need the app variable, to prevent looping (circular imports).
# We put it after the app variable (object).
# models will be used to define the structure of the database.
# babel addon has special decorator, it can be invoked on a request
@babel.localeselector
def get_locale():
    # accept_languages is an attribute of Flask's request object
    # it provides a high-level interface to work with
    # the Accept-Language header that clients send with a request
    # Accept-Language header is set by browser, the browser has setting
    # to choice which language to get, for exa.:
    # Accept-Language: da, en-gb;q=0.8, en;q=0.7;
    # where float numbers are weight of importance, preference.
    # best_match(app.config['LANGUAGES']) is just limiting the choice
    # to ones we have set in our server.

    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # or force it by:
    # return 'pl'


from app import models

# here is the form module used by Flask's WTForms
# python classes are used to represent web forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	# putting DataRequired() in [] because it's one of validator, validators input requires list
	# DataRequired() check if field is not empty
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sing In')

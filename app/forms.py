# here is the form module used by Flask's WTForms
# python classes are used to represent web forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length


class LoginForm(FlaskForm):
	# putting DataRequired() in [] because it's one of validator, validators input requires list
	# DataRequired() check if field is not empty
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sing In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	# When you add any methods that match the pattern validate_<field_name>,
	# WTForms takes those as custom validators and invokes them in addition to the stock validators
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')
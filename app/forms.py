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

	def __init__(self, original_username, *args, **kwargs):
		# thanks to super() built-in method our __init__ can use username, about_me... arguments as *args, **kwargs
		# along of newly created original_username that can be defined as EditProfileForm(current_user.username)
		# this is an overloaded constructor
		# this username is saved as an instance variable, and checked in the validate_username()
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')


class PostForm(FlaskForm):
	post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

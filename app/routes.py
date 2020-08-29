from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm


# @app refers to imported above app module, .route is a method that can be used as decorator to connect URLs
# @ are decorators; def under them, is created by them, a view function
# def index(), here is the name you would use in a url_for() call to get the URL
@app.route('/')
@app.route('/index')
@login_required
def index():
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Where is Garfield?'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'I found Garfield!'
		},
		{
			'author': {'username': 'Carol'},
			'body': 'What a good day.'
		}
	]
	return render_template('index.html', title='Home', posts=posts)


# default is GET method but we want more of it because GET is mainly used for getting things from server
# and our application post things to it so we are using POST too, we are putting it in a methods in the decorator
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Incorrect username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		# Flask provides a request variable that contains all the information that the client sent with the request
		# The request.args attribute exposes the contents of the query string in a friendly dictionary format
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect('index')
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		#  there is no db.session.add() before the commit, consider that when you reference current_user,
		#  Flask-Login will invoke the user loader callback function, which will run a database query
		#  that will put the target user in the database session. So you can add the user again in this function,
		#  but it is not necessary because it is already there.
		db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	# validation works on 'POST' level, if something is incorrect
	# if it is valid then pressing the button does:
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	# when the form is requested by the first time it fills automatically from with database's data
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form = form)

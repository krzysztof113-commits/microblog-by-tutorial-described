from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


# @app refers to imported above app module, .route is a method that can be used as decorator to connect URLs
# @ are decorators; def under them, is created by them, a view function
@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Krzysztof'}
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
	return render_template('index.html', title='Home', user=user, posts=posts)


# default is GET method but we want more of it because GET is mainly used for getting things from server
# and our application post things to it so we are using POST too, we are putting it in a methods in the decorator
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)

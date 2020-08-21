from flask import render_template
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

@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Sign In', form=form)

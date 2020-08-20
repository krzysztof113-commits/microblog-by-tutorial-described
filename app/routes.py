from flask import render_template
from app import app


# @app refers to imported above app module, .route is a method that can be used as decorator to connect URLs
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

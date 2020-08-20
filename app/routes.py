from app import app


# @app refers to imported above app module, .route is a method that can be used as decorator to connect URLs
@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Krzysztof'}
	return '''
<html>
	<head>
		<title>Homepage - Microblog</title>
	</head>
	<body>
		<h1>Hello, ''' + user['username'] + '''!</h1>
	</body>
</html>'''

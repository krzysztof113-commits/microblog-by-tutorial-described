from app import app


# @app refers to imported above app module, .route is a method that can be used as decorator to connect URLs
@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"

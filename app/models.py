from datetime import datetime
from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	# posts is what is necessary to display user of post which has some relationship with it, it's gonna be post.author
	# (for post in posts: print(post.author)), backref is a name of object, the alias for user, not a Column
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	# the way how the record of the table (object) is printed
	def __repr__(self):
		return '<User {}>'.format(self.username)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	# adding function name rather than its instance (datetime.utc now()) so it can be user many times
	# indexing it to search, organise etc. easier, faster
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

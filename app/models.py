from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
# we need to add special decorator so the flask_login extension can read database values
# it is good since flask_login can work for every database then, does not need to know how to read it
from app import login
from hashlib import md5

# Since this is an auxiliary table has only foreign keys, I created it without an associated model class.
followers = db.Table('followers',
					db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
					db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# UserMixin is a class 'template' that allows us to fulfill the (only) requirement of flask_login extension
# in order to make it works, User record needs to have is_authenticated, is_active (verified), is_anonymous and
# get_id() (a method that returns a unique identifier for the user as a string (python 3) or unicode (python 2)
# is_anonymous is for special anonymous user, by default its value is False
# we could add the Columns/methods manually nut it's easier to add UserMixin into the database model
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	# posts is what is necessary to display user of post which has some relationship with it, it's gonna be post.author
	# (for post in posts: print(post.author)), backref is a name of object, the alias for user, not a Column
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	followed = db.relationship(
		# 'User' is the right side entity of the relationship
		# secondary configures the association table used for this relationship, which I defined right above this class
		'User', secondary=followers,
		# primaryjoin indicates the condition that links the left side entity
		# the followers.c.follower_id expression references the follower_id column of the association table
		primaryjoin=(followers.c.follower_id == id),
		# secondaryjoin indicates the condition that links the right (the followed user) with the association table
		secondaryjoin=(followers.c.followed_id == id),
		# backref defines how this relationship will be accessed from the right side entity.
		# From the left side, the relationship is named followed,
		# so from the right side I am going to use the name followers
		# first lazy is for the backref (right side), other is for followed (left side)
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	# the way how the record of the table (object) is printed
	def __repr__(self):
		return '<User {}>'.format(self.username)

	# method of setting password ( your_user.set_password('my password') ) - then the server storages only hash
	# it is more secure than to storage raw passwords that can leak
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		# we need to take specific column name we are going to filter, self.followed has list of followers records
		return self.followed.filter(
			followers.c.followed_id == user.id).count() > 0


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	# adding function name rather than its instance (datetime.utc now()) so it can be user many times
	# indexing it to search, organise etc. easier, faster
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


# I thought that what to decorator does is to firstly load the user - make it's state active etc then return it
# but it can get in between since decorators are usually somewhere between the class
# so info about user is being firstly applied then our decorated function does what it should so flask_login can work
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

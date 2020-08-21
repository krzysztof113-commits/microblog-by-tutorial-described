import os

class Config(object):
	# An environment variable is a variable whose value is set outside the program,
	# typically through functionality built into the operating system or microservice.
	# Here is cryptographic key that is used by many applications and flask extensions (e.g. tokens or signatures).
	# WTForms uses it to encrypt against Cross-Site Request Forgery (CSRF) attacks. Only admins know the key.
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

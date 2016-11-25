import os

basedir = os.path.abspath(os.path.dirname(__file__))

ADMINS = ['saulu.tracker@gmail.com']

class Config:
	WTF_CSRF_ENABLED = True
	SECRET_KEY = 'The sky is not blue at night'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'saulu.tracker@gmail.com'
	MAIL_PASSWORD = 'tracker.saulu'


	@staticmethod
	def init_app(app):
		pass

class DevelopmetConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

config = {
	'development': DevelopmetConfig,
	'default': DevelopmetConfig
}
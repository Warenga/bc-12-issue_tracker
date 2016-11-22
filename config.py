import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'The sky is not blue at night'
	SQLALCHEMY_TRACK_MODIFICATIONS = True

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
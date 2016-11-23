import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'The sky is not blue at night'
	SQLALCHEMY_TRACK_MODIFICATIONS = True

		
	# # static database declarations
	# 	# Roles
	# admin_role = Role(name='Admin')
	# user_role = Role(name='User')

	# db.session.add(admin_role)
	# db.session.commit()

	# 	# Admin users
	# admin_operations = User(username='admin', email='admin_operations@gmail.com', 
	# 							department='Operations', password='operations', role=admin_role)
	# admin_finance = User(username='admin', email='admin_finance@gmail.com', 
	# 							department='Finance', password='finance', role=admin_role)

	# db.session.add_all([admin_operations, admin_finance])
	# db.session.commit()

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
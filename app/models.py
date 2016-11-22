import hashlib
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin, current_app
from flask import request

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

	users =  db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True)
	username = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(128))
	first_name = db.Column(db.String(64))
	second_name = db.Column(db.String(64))
	department = db.Column(db.String(20))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	issues = db.relationship('Issues', backref='raised_by', lazy='dynamic')
	
	def __repr__(self):
		return '%r' % self.username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

class Issues(db.Model):
	__tablename__= 'issues'
	issue_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	description = db.Column(db.Text)
	department = db.Column(db.String(20))
	priority = db.Column(db.String(20))
	raised_by = db.Column(db.String(20))
	assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
	state = db.Column(db.Boolean(), default=False)
	progress = db.Column(db.String(20))



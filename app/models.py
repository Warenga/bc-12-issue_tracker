# -*- coding: utf-8 -*-

import hashlib
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import session

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

	users =  db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True)
	username = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))
	first_name = db.Column(db.String(64))
	second_name = db.Column(db.String(64))
	department = db.Column(db.String(20))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	issue = db.relationship('Issues', backref='raised_by',  lazy='immediate')
	
	def __repr__(self):
		return self.username.encode('utf-8')


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
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	description = db.Column(db.Text(100))
	department = db.Column(db.String(20))
	priority = db.Column(db.String(20))
	assigned_to = db.Column(db.String(20))
	state = db.Column(db.String(10))
	progress = db.Column(db.String(20))
	comment = db.Column(db.Text(100))
	raised_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	states = db.relationship('State', backref='issue_state',  lazy='immediate')


	def __repr__(self):
		return '%r' % self.title

class State(db.Model):
	__tablename__ = 'states'
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(10))
	issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))

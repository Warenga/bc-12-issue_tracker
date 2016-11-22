from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from ..models import User
from .forms import SigninForm, SignupForm
from flask.ext.login import login_user, logout_user

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
	user_form = SigninForm()
	if user_form.validate_on_submit():
		user = User.query.filter_by(username=user_form.username.data).first()
		if user is not None and user.verify_password(user_form.password.data):
			flash('Welcome %s' % user.username)
			login_user(user, user_form.remember_me.data)
			return redirect(url_for('main.homepage'))
		flash('Invalid username or password')
	return render_template('auth/signin.html', user_form=user_form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	user_form = SignupForm()
	if user_form.validate_on_submit():
		user = User(first_name=user_form.first_name.data,
					second_name=user_form.second_name.data,
					email=user_form.email.data,
					username=user_form.username.data,
					password=user_form.password.data,
					department=user_form.department.data,
					role_id=2)
		db.session.add(user)
		db.session.commit()
		flash('Successful Registration')
		return redirect(url_for('auth.signin'))
	
	return render_template('auth/signup.html', user_form=user_form)
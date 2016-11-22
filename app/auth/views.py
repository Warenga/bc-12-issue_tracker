from flask import render_template, redirect, url_for, request
from . import auth
from .. import db
from ..models import User
from .forms import SigninForm, SignupForm

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
	user_form = SigninForm()
	if user_form.validate_on_submit():
		user = User.query.filter_by(username=user_form.username.data)
		if user is not None and user.verify_password(form.password.data):
			flash('Welcome %s' % user.username)
			login_user(user, form.remember_me.data)
			return 'Successful login'
		flash('Invalid username or password')
	return render_template('auth/signin.html', user_form=user_form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	user_form = SignupForm()
	user_form.department.choices = [(1,'Operations'), (2,'Finance'), (3,'Training'), (4,'Recruitment'), (5,'Success'), (6,'Sales'), (7,'Marketing')]
	if user_form.validate_on_submit():
		user = User(first_name=form.first_name.data,
					second_name=form.second_name.data,
					email=form.email.data,
					username=form.username.data,
					password=form.password.data,
					department=form.department.data)
		db.session.add(user)
		flash('Successful Registration')
		return redirect(url_for('auth.signin'))
	
	return render_template('auth/signup.html', user_form=user_form)
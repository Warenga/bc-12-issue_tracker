from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from ..models import User
from .forms import SigninForm, SignupForm
from flask.ext.login import login_user, logout_user, current_user, login_required

@auth.route('/')
def landing_page():
	return render_template('landing_page.html')

@auth.route('/sign_in', methods=['GET', 'POST'])
def login():
	user_form = SigninForm()
	if user_form.validate_on_submit():
		user = User.query.filter_by(username=user_form.username.data).first()
		if user is not None and user.verify_password(user_form.password.data):
			login_user(user, user_form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.home_page'))
		flash('Invalid username or password')
	return render_template('auth/sign_in.html', user_form=user_form)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
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
		return redirect(url_for('auth.login'))
	return render_template('auth/sign_up.html', user_form=user_form)

@auth.route('/sign_out')
@login_required
def sign_out():
	logout_user()
	return redirect(url_for('auth.login'))

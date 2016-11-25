from flask import render_template, redirect, url_for, request, flash, session
from . import auth, twitter
from . import auth
from .. import db
from ..models import User
from .forms import SigninForm, SignupForm
from flask.ext.login import login_user, logout_user, current_user, login_required

@auth.route('/')
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

@twitter.tokengetter
def get_twitter_token():
	if 'twitter oauth' in session:
		resp = session['twitter_oauth']
		return resp['oauth_token'], resp['oauth_token_secret']

@auth.route('/twitter-login')
def twitter_login():
	callback_url = url_for(
		'auth.twitter_oauthorized',
		next= request.args.get('next'))
	return twitter.authorize(callback=callback_url or request.referrer or None)

@auth.route('/oauthorized')
def twitter_oauthorized():
	resp = twitter.authorized_response()
	if resp is None:
		flash('You denied the request to sign in')
		redirect(url_for('main.login'))
	else:
		session['twitter_oauth']= resp
	this_user = User.query.filter_by(username=resp['screen_name']).first()
	if this_user is None:
		new_user = User(username=resp['screen_name'],
			password=resp['oauth_token_secret'])
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
	else:
		login_user(this_user)
	return redirect(url_for('main.home_page'))

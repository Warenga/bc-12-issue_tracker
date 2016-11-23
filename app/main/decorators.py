from functools import wraps
from flask.ext.login import current_user
from flask import flash, redirect, url_for

def required_roles(*roles):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if current_user.role_id != 1:
				flash('Cannot access! Admin only', 'error')
				return redirect(url_for('.homepage'))
			return f(*args, **kwargs)
		return wrapped
	return wrapper


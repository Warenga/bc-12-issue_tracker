from functools import wraps

def required_roles(*roles):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if get_current_user_role() not in roles:
				flash('Authentication error, please check your details and try again', 'error')
				return redirect(url_for('.homepage'))
			return f(*args, **kwargs)
		return wrapped
	return wrapper

	def get_current_user_roles():
		return g.user.role
from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User
from wtforms import ValidationError

class SigninForm(Form):
	username = StringField('Username', validators=[Required(), Length(1, 30)])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log in')

class SignupForm(Form):
	first_name = StringField('First name', validators=[Required(), Length(1, 20)])
	second_name = StringField('Second name', validators=[Required(), Length(1, 20)])
	username = StringField('Username', validators=[Required(), Length(1, 30)])
	email = StringField('Email', validators=[Required(), Length(1, 50), Email()])
	password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password', validators=[Required()])
	department = SelectField('Department', choices = [('Operations','Operations'), ('Finance','Finance'),
									('Training','Training'), ('Recruitment','Recruitment'),
									('Success','Success'), ('Sales','Sales'),
									('Marketing','Marketing')])
	submit = SubmitField('Sign up')
	

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

	

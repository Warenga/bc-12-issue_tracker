from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextField, RadioField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import Issues
from wtforms import ValidationError
from flask.ext.login import current_user

class IssueForm(Form):
	title = StringField('Title', validators=[Required()])
	description = TextField('Description')
	department = SelectField('Department', choices = [('Operations','Operations'), ('Finance','Finance'),
									('Training','Training'), ('Recruitment','Recruitment'),
									('Success','Success'), ('Sales','Sales'),
									('Marketing','Marketing')])
	priority = RadioField('Priority', choices=[('High','High'), ('Medium','Medium'), ('Low','Low')])
	submit = SubmitField('Submit')

class MarkIssueForm(Form):
	assigned_to = SelectField('Assign to: ')
	progress = SelectField('Progress', choices=[('not assigned', 'not assigned'),
						('resolved','resolved'), ('in-progress','in-progress')])
	comment = TextField('Comment')
	submit = SubmitField('Submit')

	def __init__(self):
		super(MarkIssueForm, self).__init__()

		from ..models import User
		self.assigned_to.choices = [(user.email, user.username) for user in
				(User.query
				.filter_by(role_id=3)
				.filter_by(department=current_user.department)
				)]

class ResolveForm(Form):
	progress = StringField('Progress')
	submit = SubmitField('Submit')


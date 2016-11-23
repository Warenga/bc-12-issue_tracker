from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextField, RadioField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import Issues
from wtforms import ValidationError

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
	assigned_to = StringField('Assign to: ')
	progress = SelectField('Progress', choices=[('resolved','resolved'), ('in-progress','in-progress'), ('not assigned','not assigned')])
	comment = TextField('Comment')
	submit = SubmitField('Submit')


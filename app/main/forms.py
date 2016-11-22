from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextField, RadioField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import Issues
from wtforms import ValidationError

class IssueForm(Form):
	title = StringField('Title', validators=[Required()])
	description = TextField('Description')
	department = SelectField('Department', coerce=int, choices = [(1,'Operations'), (2,'Finance'),
									(3,'Training'), (4,'Recruitment'),
									(5,'Success'), (6,'Sales'),
									(7,'Marketing')])
	priority = RadioField('Priority', choices=[('High','High'), ('Medium','Medium'), ('Low','Low')])
	submit = SubmitField('Submit')
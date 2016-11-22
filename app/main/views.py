from flask import render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import Issues
from .forms import IssueForm
from flask.ext.login import current_user

@main.route('/main', methods=['GET', 'POST'])
def homepage():
	issue_form = IssueForm()
	if issue_form.validate_on_submit():
		issue = Issues(title=issue_form.title.data,
						description=issue_form.description.data,
						department=issue_form.department.data,
						priority=issue_form.priority.data,
						raised_by = current_user._get_current_object()
						)
		db.session.add(issue)
		db.session.commit()
		flash('You issue has been raised. You shall get feedback soon')
		return redirect(url_for('.homepage'))
	return render_template('home.html', issue_form=issue_form)


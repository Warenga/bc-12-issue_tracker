from flask import session, g, render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import Issues, State, User
from .forms import IssueForm, MarkIssueForm, ResolveForm
from flask.ext.login import current_user, login_required
from .decorators import required_roles
from ..email import notify_user, assign_issue

@main.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
	if current_user.role.id == 1:
		open_issues = (Issues.query 
						.filter_by(department=current_user.department)
						.filter_by(state='open')
						)
		closed_issues = (Issues.query 
						.filter_by(department=current_user.department)
						.filter_by(state='closed')
						)
	elif current_user.role.id == 3:
		open_issues = (Issues.query
						.filter_by(assigned_to=current_user.email)
						.filter_by(state='open')
						)
		closed_issues = (Issues.query
						.filter_by(assigned_to=current_user.email)
						.filter_by(state='closed')
						)
	else:
		open_issues = Issues.query.filter_by(state='open').all()
		closed_issues = Issues.query.filter_by(state='closed').all()
	return render_template('home.html', open_issues=open_issues, closed_issues=closed_issues)

@main.route('/new_issue', methods=['GET', 'POST'])
@login_required
def new_issue():
	issue_form = IssueForm()
	if issue_form.validate_on_submit():
		issue = Issues(title=issue_form.title.data,
						description=issue_form.description.data,
						department=issue_form.department.data,
						priority=issue_form.priority.data,
						raised_by = current_user._get_current_object(),
						state= 'open'
						)
		db.session.add(issue)
		db.session.commit()
		state = State(state=issue.state, issue_id=issue.id)
		db.session.add(state)
		db.session.commit()
		flash('You issue has been raised. You shall get feedback soon')
		return redirect(url_for('.homepage'))
	return render_template('new_issue.html', issue_form=issue_form)

@main.route('/state/<int:id>', methods=['GET', 'POST'])
@login_required
def issue_state(id):
	issue = Issues.get_or_404(id)
	state = issue.state.order_by.all()
	return render_template('new_issue.html', issues=[issue], states=state)

@main.route('/admin_view/<int:id>', methods=['GET','POST'])
@login_required
@required_roles(1)
def check_issues(id):
	issue = Issues.query.get_or_404(id)
	check_form = MarkIssueForm()
	if request.method == 'POST' and check_form.validate():
		issue.assigned_to = check_form.assigned_to.data
		issue.progress = check_form.progress.data
		if issue.progress == 'resolved':
			issue.state = 'closed'
		else:
			issue.state = 'open'
		issue.comment = check_form.comment.data
		db.session.add(issue)
		db.session.commit()
		notify_user(issue)
		assign_issue(issue)
		return redirect(url_for('.homepage'))
	return render_template('check_issue.html', issues=[issue], check_form=check_form)

@main.route('/issue/progress/<int:id>', methods=['GET', 'POST'])
@login_required
@required_roles(3)
def resolve(id):
	issue = Issues.query.get_or_404(id)
	resolve_form = ResolveForm() 
	if resolve_form.validate_on_submit():
		issue.progress = 'resolved'
		if issue.progress == 'resolved':
			issue.state = 'closed'
		else:
			issue.state = 'open'
		db.session.add(issue)
		db.session.commit()
		return redirect(url_for('.homepage'))
	return render_template('home.html', issues=[issue], resolve_form=resolve_form)

	

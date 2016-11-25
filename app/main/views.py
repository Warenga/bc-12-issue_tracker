from flask import session, g, render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import Issues, User
from .forms import IssueForm, MarkIssueForm, ResolveForm, SuperForm, RoleForm
from flask.ext.login import current_user, login_required
from .decorators import required_roles
from ..email import notify_user, assign_issue

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
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
	elif current_user.role.id == 4:
		open_issues = Issues.query.all()
		closed_issues = Issues.query.all()
	else:
		open_issues = (Issues.query
						.filter_by(raised_by=current_user)
						.filter_by(state='open')
						)
		closed_issues = (Issues.query
						.filter_by(raised_by=current_user)
						.filter_by(state='closed')
						)
	return render_template('home.html', open_issues=open_issues, closed_issues=closed_issues)

@main.route('/home_social', methods=['GET', 'POST'])
def home_social():
	role_form = RoleForm()
	if role_form.validate_on_submit():
		user = User(role_id=role_form.role.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('.home_page'))
	return render_template('specify.html', role_form=role_form)

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
		flash('You issue has been raised. You shall get feedback soon')
		return redirect(url_for('.home_page'))
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
		return redirect(url_for('.home_page'))
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
		return redirect(url_for('.home_page'))
	return render_template('home.html', issues=[issue], resolve_form=resolve_form)

@main.route('/add_trainer', methods=['GET', 'POST'])
@login_required
@required_roles(4)
def add_trainer():
	fixer_form = SuperForm()
	if fixer_form.validate_on_submit():
		user = User(email=fixer_form.email.data,
					username=fixer_form.username.data,
					password=fixer_form.password.data,
					department=fixer_form.department.data,
					role_id=3)
		db.session.add(user)
		db.session.commit()
		flash('Successful added')
		return redirect(url_for('main.view'))
	return render_template('add_fixer.html', fixer_form=fixer_form)

@main.route('/add_admin', methods=['GET', 'POST'])
@login_required
@required_roles(4)
def add_admin():
	admin_form = SuperForm()
	if admin_form.validate_on_submit():
		user = User(email=admin_form.email.data,
					username=admin_form.username.data,
					password=admin_form.password.data,
					department=admin_form.department.data,
					role_id=1)
		db.session.add(user)
		db.session.commit()
		flash('Successful added')
		return redirect(url_for('main.view'))
	return render_template('add_admin.html', admin_form=admin_form)

@main.route('/view', methods=['GET', 'POST'])
@login_required
@required_roles(4)
def view():
	users = User.query.all()
	return render_template('view.html', users=users)







	

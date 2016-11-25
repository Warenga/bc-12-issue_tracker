# bc-12-issue_tracker
Andela Bootcamp 12 final project

# Issue Tracker

An issue tracker application that allows issues to be raised to the correct admin and solved.

Written in <strong>python language</strong> using <strong>flask framework</strong>. The UI is <strong>Jinja2 templates</strong> incorporated in <strong>flask twitter-bootstrap</strong>. The database is <strong>SQLAlchemy</strong> in <strong>SQlite</strong>.


Click <a href="http://saulu.herokuapp.com"> here</a> to view the staged version. Login with twitter or signup.


### What it does
------------------------------------------------

	1. User Registration
	2. User Sign In
	3. Login in with Twitter 
	4. Allows user to raise an issue
	5. Issue sent to the admin of the assigned department.
	6. Admin login and views all issues sent to his department.
	7. Admin assigns issue to a fixer.
	8. Admin sets issue progress to resolved or in progress.
	9. Email notification sent to User when Admin assigns an sets progress.
	10. Email notification sent to Fixer email when Admin assigns an issue to fixer.
	11. Fixer can login and view issues assigned to him or her.
	12. Issue once resolved is moved to closed table. Meaning it is resolved.
	13. Super Admin able to add a fixer and admin.
	14. Super Admin able to view all issues and view all users. 

### What needs to be added
----------------------------------------------

	1. Editing of issues raised
	2. Error pages

### Bugs
----------------------------------------------
	
	1. Twitter login works but cannot view issues as role id is not assigned.

### Admin Login Details
----------------------------------------------
To login as Admin the username is admin_<department> password <department>.
for example Sales department: username = <i>admin_sale</i> password = <i>sale</i>

Super Admin:
username = super
password = super
	

### Run it locally
--------------------------------------------------
Have python 2.7 or 3 installed in your machine

<strong=>Clone this repository</strong>
	https://github.com/Warenga/bc-12-issue_tracker.git

<strong>Create a virtualenv</strong>

<strong>Install the requirements</strong>

	$pip install -r requirements.txt

<strong>Initialize the database</strong>

	$pip manage.py db init

<strong>Construct and upgrade the database</strong>

	$ python manage.py db upgrade

<strong>Run the server</strong>

	$ python manage.py runserver
	

Enjoy!


		


from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)
#app.secret_key = b'\x1f\x8d\xaf\xe3\xec\x01 \xa1\x95\x99Kf\xdc\xe9G\x15\xa0C\x9e\x9bf\x08\x9c;'
app.secret_key = os.environ.get('SECRET_KEY').encode()



@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())


@app.route('/create', methods=['GET', 'POST'])
def create():
    # If user is not logged in, go to login page
    # If the method is POST:
    #    then use the name that the user submitted to create a
    #    new task and save it
    #    Also, redirect the user to the list of all tasks
    # Otherwise, just render the create.jinja2 template
    if 'username' not in session:
        return redirect(url_for(login))

    if request.method == 'POST':
        task = Task(name=request.form['name'])
        task.save()
        # why do you sometimes render and sometimes return a redirect?
        return(redirect(url_for('all_tasks')))
    else:
        return render_template('create.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is attempting to submit the login form (method is POST)
    #    Find a user from the database that matches the username provided
    # in the form submission
    if request.method == 'POST':
        try:
            #user = User.select().where(User.name == request.form['name']).get()
            # note this alternate, shorter syntax suggeted in docs:
            user = User.get(User.name == request.form['name'])
            #    If you find such a user and their password matches the
            # provided password:
            if user and pbkdf2_sha256.verify(request.form['password'], user.password):
                # Then log the user in by settings session['username']
                # to the users name
                session['username'] = request.form['name']
                #And redirect the user to the list of all tasks
                return(redirect(url_for('all_tasks')))
            else:
            # Else: Render the login.jinja2 template and include an error message
                return render_template('login.jinja2', error="Incorrect password.")
        except (AttributeError, Exception) as e:
            # how do I find out what kind of exception is raised?
            # was expecting the peewee exception DoesNotExist but did not work
            return render_template('login.jinja2', error="User not found.")
    else:
        # Else the user is just trying to view the login
        # so render the login.jinja2 template
        return render_template('login.jinja2')

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    # If the visitor is not logged in as a user:
        # Then redirect them to the login page
    if 'username' not in session:
        return redirect(url_for(login))

    # if the request method is post
    if request.method == 'POST':
        # Then retrieve the username from the session and find its user
        user = User.get(User.name == session['username'])
        # Retrieve the task_id from the form submission
        # and use it to find the associated task
        task = Task.get(request.form['task_id'] == Task.id)
        # Update the task to indicate that it has been completed
        # at datetime.now() by the current user.
        # update is a peewee function
        task.update(performed_by=user.name, performed=datetime.now())
        #task.execute() # throws an error
        print(type(task))
        Task.update(performed=datetime.now(), performed_by=user)\
            .where(Task.id == request.form['task_id'])\
            .execute()

    # Retrieve a list of all incomplete tasks & pass to renderer
    incomplete = Task.select().where(Task.performed.is_null())
    return render_template('incomplete.jinja2', tasks=incomplete)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

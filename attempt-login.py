@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is attempting to submit the login form (method is POST)
    #    Find a user from the database that matches the username provided
    # in the form submission
    if request.method == 'POST':
        try:
            user = User.select().where(User.name == request.form['name']).get()
            # user = User.get(User.name == request.form['name'])
            #    If you find such a user and their password matches the
            # provided password:
            if user and pbkdf2_sha256.verify(user.password, request.form['password']):
                # Then log the user in by settings session['username']
                # to the users name
                session['username'] = request.form['name']
        #        And redirect the user to the list of all tasks
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

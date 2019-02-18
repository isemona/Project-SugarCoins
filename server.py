'''Project Sugar Coins'''

from flask import Flask, flash, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

# need to allow access to database
from model import connect_to_db, db, Gender, User, Food, Sugar

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "willywonka"

# Normally, if you use an undefined variable in Jinja2, it fails silently.

@app.route('/')
def index():
    """Homepage"""


    return render_template("homepage.html")



@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Show form for user signup and process."""

    if request.method == 'POST':
        fname = request.form["fname"]
        print(fname)
        lname = request.form["lname"]
        print(lname)
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        print(password)
        gender = request.form["gender"]

        # age = int(request.form["age"]) maybe this should be a view?
        # weight = request.form["weight"]
        # blood_glucose = request.form["blood-glucose"]
        name = " ".join([fname,lname])
        print(name)

        new_user = User(name=name, email=email, password=password, gender_code=gender)

        print(new_user)

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {name} added.")
        return redirect(f"/user_dashboard/{new_user.user_id}")

    return render_template("register_form.html")

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Show login form and process."""

    
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No such user")
            return redirect("/login")

        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("Logged in")
        return redirect(f"/user_dashboard/{user.user_id}")

    return render_template("login_form.html")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/user_intake', methods=['GET', 'POST'])
def intake_form():
    """Show intake form and process."""

    if request.method == 'POST':


        if 'name' in session:
            user = User.query.filter_by(name=name).first()
            user_id = user.user_id

        user_food = request.form["food"]

        if 'user_food' not in session:
            session['user_food'] = sugar.food
        
        cost = request.form["cost"]

        date_time = request.form["date_time"]
        date_time = datetime.datetime("%Y-%m-%d")

        notes = request.form["notes"] 

    
        sugar = Sugar(user_id=sugar.user_id,
                    user_food=sugar.food,
                    cost=cost,
                    date_time=date_time,
                    notes=notes,
                    )

        # user = query.get from session user logged in 
        # once you have the food and user you'll create a Sugar(notes=notes) to add the notes 
        # sugar.user = user in session to query for 
        # sugar.food = user_food
        # use sql magic to figure out the variables and their values for you


        db.session.add(sugar)
        
        db.session.commit()

        flash(f"User {name} added.")
        return redirect(f"/user_dashboard/{new_user.user_id}")

    return render_template("user_intake.html")


@app.route('/user_dashboard', methods=['GET'])
def user_dashboard():
    """Show user dashboard."""


    return render_template("user_dashboard.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")



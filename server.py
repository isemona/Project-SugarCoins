'''Project Sugar Coins'''

from flask import Flask, flash, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from datetime import datetime

# need to allow access to database
from typing import Any

from model import connect_to_db, db, Gender, User, Food, Sugar, Weight, Glucose

from query import *
from twilio.twiml.messaging_response import MessagingResponse

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
        lname = request.form["lname"]
        name = " ".join([fname, lname])
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]
        phone = request.form["pnum"]

        # age = int(request.form["age"]) # maybe this should be under proflie

        new_user = User(name=name, email=email, password=password, gender_code=gender, phone=phone)

        print(new_user)

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {name} added.")

        return redirect("/login")

    return render_template("register_form.html")


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Show login form and process."""

    if request.method == 'POST':
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        print(password)
        user = User.query.filter_by(email=email).first()
        print(user)

        if not user:
            flash("No such user")
            return redirect("/login")

        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")

        # del session["user_id"]
        session["user_id"] = user.user_id  # this instantiates the session library to include user_id
        session['user'] = user.name  # this instantiates the session library to include user name

        flash("Logged in")
        return redirect(f"/user_intake/{user.user_id}")

    return render_template("login_form.html")


@app.route('/logout')
def logout():
    """Log out."""
    flash("Logged Out.")
    del session["user_id"]

    return redirect("/")


@app.route('/user_intake/<int:user_id>', methods=['GET', 'POST'])
def intake_form(user_id):
    """Show intake form and process."""

    if request.method == 'POST':

        if 'user_id' in session:
            user = User.query.filter_by(user_id=session["user_id"]).first()
            user_id = user.user_id

            cost = request.form["cost"]
            food = request.form["food"]

            user_food = Food.query.filter(Food.food_name == food, Food.cost == cost).first()
            if user_food:
                print(user_food)
                print(user_food.food_id)

            if not user_food:  # if the query comes out empty
                user_food = Food(food_name=food, cost=cost)
                print(user_food)
                db.session.add(user_food)
                db.session.commit()

            date_time = datetime.utcnow()

            notes = request.form["notes"]

        sugar = Sugar(user_id=user_id,
                      food_id=user_food.food_id,
                      notes=notes,
                      date_time=date_time,
                      )

        print(sugar)

        db.session.add(sugar)
        db.session.commit()

        # flash(f"Food {food} added.")
        return redirect(f"/user_dashboard/{user_id}")  # route to be a string

    return render_template("user_intake.html", user_id=user_id)


@app.route('/user_dashboard/<int:user_id>', methods=['GET', 'POST'])
def user_dashboard_main(user_id):
    """Show user dashboard."""

    # user_id = session["user_id"] # no need this here because it is already passed in as a variable
    foods = get_user_list_of_food(session)
    allowance = get_user_allowance(session)
    daily_in = get_user_daily_spending(session)

    # if request.method == 'POST':
    #     weight = int(request.form["weight"])
    #     glucose = int(request.form["blood-glucose"])
    #
    #     date_time = datetime.utcnow()
    #
    #     user_weight = Weight(user_id=user_id, current_weight=weight, date_time=date_time)
    #     db.session.add(user_weight)
    #     db.session.commit()
    #
    #     user_glucose = Glucose(user_id=user_id, current_glucose=glucose, date_time=date_time)
    #     db.session.add(user_glucose)
    #     db.session.commit()

    if request.method == 'POST':
        if request.form.get('weight'):
            weight = int(request.form["weight"])

            date_time = datetime.utcnow()

            user_weight = Weight(user_id=user_id, current_weight=weight, date_time=date_time)
            db.session.add(user_weight)
            db.session.commit()

        if request.form.get("blood-glucose"):

            glucose = int(request.form["blood-glucose"])

            date_time = datetime.utcnow()

            user_glucose = Glucose(user_id=user_id, current_glucose=glucose, date_time=date_time)
            db.session.add(user_glucose)
            db.session.commit()

    weight = get_user_current_weight(session)

    glucose = get_user_current_glucose(session)

    average = get_average_spending(session)

    return render_template("user_dashboard.html", foods=foods, allowance=allowance, user_id=user_id, daily_in=daily_in,
                           weight=weight, glucose=glucose, average=average)


@app.route('/user_weight.json', methods=['GET', 'POST'])
def user_weight_trends():
    """Show user dashboard."""

    month_dict = {
        1.0: 'Jan',
        2.0: 'Feb',
        3.0: 'Mar',
        4.0: 'Apr',
        5.0: 'May',
        6.0: 'Jun',
        7.0: 'Jul',
        8.0: 'Aug',
        9.0: 'Sep',
        10.0: 'Oct',
        11.0: 'Nov',
        12.0: 'Dec'
    }

    weights = get_user_weight(session)

    month_day = []
    monthly_values = []

    for weight in weights:
        months = month_dict[weight[1]]
        days = str(int(weight[2])) # int() will floor your float
        month_day.append(months + " " + days)
        monthly_values.append(weight[3])

    data_dict = {
        "labels": month_day,

        "datasets": [
            {
                "label": 'Weight Over Time',
                "data": monthly_values,
                "backgroundColor": [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                "borderColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": "true"
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)

@app.route('/user_glucose.json', methods=['GET', 'POST'])
def user_glucose_trends():
    """Show user dashboard."""

    month_dict = {
        1.0: 'Jan',
        2.0: 'Feb',
        3.0: 'Mar',
        4.0: 'Apr',
        5.0: 'May',
        6.0: 'Jun',
        7.0: 'Jul',
        8.0: 'Aug',
        9.0: 'Sep',
        10.0: 'Oct',
        11.0: 'Nov',
        12.0: 'Dec'
    }

    glucose = get_user_glucose(session)
    month_day = []
    monthly_values = []

    for level in glucose:
        months = month_dict[level[1]]
        days = str(int(level[2]))  # int() will floor your float
        month_day.append(months + " " + days)
        monthly_values.append(level[3])



    data_dict = {
        "labels": month_day,

        "datasets": [
            {
                "label": 'Glucose Over Time',
                "data": monthly_values,
                "backgroundColor": [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                "borderColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": "true"
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)


@app.route('/trends/<int:user_id>', methods=['GET', 'POST'])
def user_trends(user_id):
    """Show user trends."""

    name = session["user"].split(" ")
    fname = name[0]

    return render_template("trends.html", fname=fname)


@app.route('/trends.json', methods=['GET', 'POST'])
def user_mood_trends():
    """Show user trends."""

    print("hello")
    print(get_user_moods(session))

    data_dict = get_user_moods(session) # array of objects


    return jsonify(data_dict)

@app.route('/user_percent_intake.json')
def user_percent_intake():
    """Show user percent daily intake."""

    # call you helper functions here
    # del session["user_id"]
    session["user_id"]

    percent = calculate_user_daily_spending_percentage(session)

    data_dict = {
        "labels": [
            "User Intake",
            "Remaining"

        ],

        "datasets": [
            {
                "label": 'Percentage of User Intake',
                "data": [100 - percent, percent],
                "backgroundColor": [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                "borderColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": "true"
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)


@app.route('/user_monthly_intake.json')
def user_monthly_intake():
    """Show user monthly intake."""

    # call you helper functions here
    # del session["user_id"]
    session["user_id"]

    month_dict = {
        1.0: 'Jan',
        2.0: 'Feb',
        3.0: 'Mar',
        4.0: 'Apr',
        5.0: 'May',
        6.0: 'Jun',
        7.0: 'Jul',
        8.0: 'Aug',
        9.0: 'Sep',
        10.0: 'Oct',
        11.0: 'Nov',
        12.0: 'Dec'
    }

    months = get_monthly_spending(session)
    monthly_labels = []
    monthly_values = []

    for month in months:
        monthly_labels.append(month_dict[month[1]])
        monthly_values.append(month[2])

    # add color hardcoded for every month
    data_dict = {
        "labels": monthly_labels,

        "datasets": [
            {
                "label": '2019 Monthly Intake',
                "data": monthly_values,
                "backgroundColor": [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                "borderColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": "true"
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.") # message sent when you need a response from the user

    return str(resp)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

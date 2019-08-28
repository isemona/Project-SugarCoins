"""Project Sugar Coins"""

from flask import Flask, flash, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from datetime import datetime
import bcrypt

# need to allow access to database
from typing import Any

from models import connect_to_db, db, Gender, User, Food, Sugar, Weight, Glucose

from query import *
from twilio.twiml.messaging_response import MessagingResponse

# turn off when not using continuously
#testing twilio 1-3 req
from send_sms import *

app = Flask(__name__)

# Normally, if you use an undefined variable in Jinja2, it fails silently.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "willywonka"

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
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("No such user")
            return redirect("/login")

        # Added encryption
        # hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # import pdb
        # pdb.set_trace()
        if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')) is False:
            flash("Incorrect password")
            return redirect("/login")

        # if bcrypt.checkpw(password.encode('utf8'), user.password) is False:
        #     flash("Incorrect password")
        #     return redirect("/login")

        session["user_id"] = user.user_id
        session['user'] = user.name

        flash("Logged in")
        return redirect(f"/user_dashboard/{user.user_id}")

    return render_template("login_form.html")


@app.route('/logout')
def logout():
    """Log out."""
    flash("Logged Out.")
    del session["user_id"]

    return redirect("/")

@app.route('/user_intake/<int:user_id>', methods=['GET', 'POST'])
def intake_form(user_id):
    """Show intake form and process on dashboard."""
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
    foods = get_lists_of_food(session)
    print(foods)
    allowance = get_user_allowance(session)
    daily_in = get_user_daily_spending(session)

    name = session["user"].split(" ")
    fname = name[0]

    return render_template("user_dashboard.html", foods=foods, allowance=allowance, user_id=user_id, daily_in=daily_in,
                           fname=fname)

@app.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    """Show user weight and glucose intake form."""
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

    return render_template("user_profile.html", user_id=user_id, weight=weight, glucose=glucose)

@app.route('/user_weight.json', methods=['GET', 'POST'])
def user_weight_trends():
    """Show user trends."""
    weights = get_user_weight(session)
    month_day = []
    monthly_values = []

    for weight in weights:
        months = month_dict[weight[1]]
        days = str(int(weight[2]))  # int() will floor your float
        month_day.append(months + " " + days)
        monthly_values.append(weight[3])

    data_dict = {
        "labels": month_day,
        "datasets": [
            {
                "label": 'Weight Over Time',
                "data": monthly_values,
                "fill": False,
                "backgroundColor": [
                    # 'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderColor": [
                    # 'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 4
            }],

        "options": {
            "legend": {
                "labels": {
                    "fontColor": 'green',
                    "fontSize": 30,
                }
            },
            # "title": {
            #     "display": True,
            #     "fontColor": 'blue',
            #     "text": 'Custom Chart Title'
            # },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "fontSize": 30,
                        # "fontColor": 'white',
                        "beginAtZero": "true"
                    }
                }],
                "xAxes": [{
                    "ticks": {
                        "fontSize": 20,
                        # "fontColor": 'white',
                        "beginAtZero": "true"
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)

@app.route('/user_glucose.json', methods=['GET', 'POST'])
def user_glucose_trends():
    """Show user trends."""
    glucose = get_user_glucose(session)
    month_day = []
    monthly_values = []

    for level in glucose:
        months = month_dict[level[1]]
        days = str(int(level[2]))
        month_day.append(months + " " + days)
        monthly_values.append(level[3])

    data_dict = {
        "labels": month_day,
        "datasets": [
            {
                "label": 'Glucose Level Over Time',
                "data": monthly_values,
                "fill": False,
                "backgroundColor": [
                    # 'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderColor": [
                    # 'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 4
            }],

        "options": {
            "legend": {
                "labels": {
                    "fontColor": 'green',
                    "fontSize": 30,
                }
            },
            # "title": {
            #     "display": True,
            #     "fontColor": 'blue',
            #     "text": 'Custom Chart Title'
            # },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "fontSize": 30,
                        # "fontColor": 'white',
                        "beginAtZero": "true"
                    }
                }],
                "xAxes": [{
                    "ticks": {
                        "fontSize": 20,
                        # "fontColor": 'white',
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
    weight = get_user_current_weight(session)
    glucose = get_user_current_glucose(session)
    average = get_average_spending(session)

    return render_template("trends.html", fname=fname, weight=weight, glucose=glucose, average=average, user_id=user_id)

@app.route('/trends.json', methods=['GET', 'POST'])
def user_mood_trends():
    """Show user trends."""
    data_dict = get_user_moods(session)

    return jsonify(data_dict)


@app.route('/user_percent_intake.json', methods=['GET', 'POST'])
def user_percent_intake():
    """Show user percent daily intake in dashboard."""
    session["user_id"]
    percent = calculate_user_daily_spending_percentage(session)
    print(percent)
    data_dict = {
        "labels": [
            "User Intake",
            "Remaining",

        ],

        "datasets": [
            {
                "label": 'Percentage of User Intake',
                "data": [percent,max(0,100-percent)],
                "backgroundColor": [
                    'rgba(75, 192, 192, 1)',
                    # 'rgba(2, 244, 240, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderColor": [
                    # 'rgba(75, 192, 192, 1)',
                    'rgba(2, 244, 240, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)

@app.route('/user_monthly_intake.json', methods=['GET', 'POST'])
def user_monthly_intake():
    """Show user monthly intake in trends."""
    session["user_id"]
    months = get_monthly_spending(session)
    monthly_labels = []
    monthly_values = []

    for month in months:
        monthly_labels.append(month_dict[month[1]])
        monthly_values.append(month[2])

    data_dict = {
        "labels": monthly_labels,


        "datasets": [
            {
                "label": 'Monthly Intake',
                "data": monthly_values,
                "backgroundColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderColor": [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                "borderWidth": 1
            }],

        "options": {
            "legend": {
                "labels": {
                    "fontColor": 'green',
                    "fontSize": 30,
                }
            },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }

    }

    return jsonify(data_dict)

@app.route('/sms_test/<int:user_id>', methods=['GET', 'POST'])
def send_balance_update(user_id):
    """Show user dashboard."""
    message = send_msg()

    return "<h1>hello</h1>"


# @app.route("/sms_test", methods=['GET', 'POST'])
# def sms_balance_update():
#     """Update the user with their current balance."""
#     # balance = send_msg
#     return render_template("user_dashboard.html") 

# @app.route("/sms", methods=['GET', 'POST'])
# def sms_ahoy_reply():
#     """Respond to incoming messages with a friendly SMS."""
#     # Start our response
#     send_msg(session)

#     return str(resp)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # turn off schedule.every and schedule.run_continuously(1) bec Twilio will charge per text
    # run the schedule time first
    # schedule.every().day.at("12:00").do(send_msg)

    #testing twilio 2-3 req
    # schedule.every(60).seconds.do(send_msg)

    
    # Turn on debugger only for testing app
    app.debug = False
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # testing twilio 3-3 req
    # schedule.run_continuously(1)

    app.run(host="0.0.0.0")

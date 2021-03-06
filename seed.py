"""Utility file to seed Sugarcoins database for demo account"""

# to randomize on list of sweets and list of grams spent per day
# https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/, arguments is a range i.e. from 1 to 26
import random

# to use the datetime library and syntax is datetime.datetime
import datetime

from sqlalchemy import func

# need to allow access to these Objects to load/seed data
from models import connect_to_db, db, Gender, User, Food, Sugar, Weight, Glucose

# connecting to database aka SQL i.e. connect_to_db(app) has 'app' app comes from ther server so this needs to be imported too
from server import app


sweets = ['snickers', 'soda', 'juice', 'M&Ms', 'yogurt', 'cereal']
reason = ['tired', 'hangry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'experiencing-loss']
password = 'testing123'
name = 'demo'
email = 'demo@sugarcoin.com'
gender = 'F'
user_id = 1
phone = '+12345678910'


def load_users():
    """Load users from Faker Library to database"""

    user = User(name=name,
                email=email,
                gender_code=gender,
                password=password,
                )
    # We need to add to the session or it won't ever be stored
    db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_gender():
    """Load users from Faker Library to database"""

    female = Gender(gender_code='F',
                    allowance=25,
                    )

    male = Gender(gender_code='M',
                  allowance=38,
                  )

    db.session.add(female)
    db.session.add(male)

    db.session.commit()


def load_food():
    """Load food from a list of sweets."""

    for _ in range(10):
        food_name = random.choice(sweets)
        cost = random.randint(1, 38)

        sweet_food = Food(food_name=food_name,
                          cost=cost,
                          )
        db.session.add(sweet_food)

    db.session.commit()


def load_sugar_intake():
    """Load sugar intake at particular time and why."""

    for _ in range(4):
        date_time = datetime.datetime(2018, 4, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 5, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 6, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 7, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 8, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 9, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 10, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 11, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 12, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 1, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(4):
        date_time = datetime.datetime(2018, 2, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    for _ in range(0):
        date_time = datetime.datetime(2018, 3, 22, 19, 12, 22)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)

    db.session.commit()

def load_weight():
    """Load weight over time."""

    date_time = datetime.datetime(2019, 1, 22, 19, 12, 22)
    current_weight = 133

    user_weight = Weight(current_weight=current_weight,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_weight)

    db.session.commit()

def load_weight_two():
    """Load weight over time."""

    date_time = datetime.datetime(2019, 2, 22, 19, 12, 22)
    current_weight = 123

    user_weight = Weight(current_weight=current_weight,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_weight)

    db.session.commit()

def load_weight_three():
    """Load weight over time."""

    date_time = datetime.datetime(2019, 3, 22, 19, 12, 22)
    current_weight = 123

    user_weight = Weight(current_weight=current_weight,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_weight)

    db.session.commit()


def load_glucose():
    """Load glucose over time."""

    date_time = datetime.datetime(2019, 1, 22, 19, 12, 22)
    current_glucose = 91

    user_glucose = Glucose(current_glucose=current_glucose,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_glucose)

    db.session.commit()

def load_glucose_two():
    """Load glucose over time."""

    date_time = datetime.datetime(2019, 2, 22, 19, 12, 22)
    current_glucose = 90

    user_glucose = Glucose(current_glucose=current_glucose,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_glucose)

    db.session.commit()

def load_glucose_three():
    """Load glucose over time."""

    date_time = datetime.datetime(2019, 3, 22, 19, 12, 22)
    current_glucose = 90

    user_glucose = Glucose(current_glucose=current_glucose,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_glucose)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    load_gender() # here we loaded Gender first
    load_users()
    load_food()
    load_sugar_intake()
    load_weight()
    load_weight_two()
    load_weight_three()
    load_glucose()
    load_glucose_two()
    load_glucose_three()

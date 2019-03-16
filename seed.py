"""Utility file to seed sugarcoins database from Faker Python"""

# to randomize on list of sweets and list of grams spent per day
# https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/, arguments is a range i.e. from 1 to 26
import random

# to use the datetime library and syntax is datetime.datetime
import datetime

# necessary imports to extract data from Faker library
from faker import Faker
from faker.providers import profile

from sqlalchemy import func  # WHAT IS THIS??

# need to allow access to these Objects to load/seed data
from model import connect_to_db, db, Gender, User, Food, Sugar, Weight, Glucose

# connecting to database aka SQL i.e. connect_to_db(app) has 'app' app comes from ther server so this needs to be imported too
from server import app

fake = Faker()

sweets = ['snickers', 'soda', 'juice', 'M&Ms', 'yogurt', 'cereal']
# alternative = ['stevia', 'orange', 'strawberry', 'blueberry', 'plum']
reason = ['tired', 'hangry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'experiencing-loss']
password = 'testing123'
name = 'Demo'
email = 'demo@gmail.com'
gender = 'F'
user_id = 1
#phone = '+14084124657'

# notes would be different for woman - ['tired', 'hungry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'hormonal-related', 'experiencing-loss']

# keeping 'hormonal-related' out because this is past data


def load_users():
    """Load users from Faker Library to database"""

    # print statement for testing
    print('Users')

    # generating 10 user profile objects
    # user_profiles = []
    # for _ in range(10):
    #     user_profiles.append(fake.profile())
    #
    # print(user_profiles)
    #
    # # accessing properties in individual objects
    # sugarholics = []
    # for user in user_profiles:
    #     sugarholics.append([user['name'], user['mail'], user['sex']])
    #
    # print(sugarholics)
    #
    # for person in sugarholics:
    #     name = person[0]
    #     email = person[1]
    #     gender = person[2]
    #     # age = person[3], user['birthdate'] => datetime.date(1991, 9, 22)

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

    # print statement for testing
    print('Gender')

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

    # print statement for testing
    print('Food')

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

    print('Sugar Intake')

    # notes = random.choice(reason)

    time = []
    for _ in range(10):
        # time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
        time.append(fake.date_between(start_date="-1y", end_date="-90d"))


    #
    for dt in time:
        date_time = dt
    #     notes = random.choice(reason)
    #     #user_id = random.randint(1, 10)
    #     food_id = random.randint(1, 10)
        notes = random.choice(reason)
        food_id = random.randint(1, 10)

        sugar_intake = Sugar(notes=notes,
                             date_time=date_time,
                             user_id=user_id,
                             food_id=food_id,
                             )

        db.session.add(sugar_intake)


    # date_time = datetime.datetime(2019, 1, 22, 19, 12, 22)




    db.session.commit()

def load_weight():
    """Load weight over time."""

    print('Weight')

    # time = []
    # for _ in range(10):
    #     time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
    #
    # for dt in time:
    #     date_time = dt
    #     user_id = 1
    #     #user_id = random.randint(1, 10)
    #     #current_weight = random.randint(100,250)
    #     user_id = 1
    #     current_weight = 133

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

    print('Weight')

    # time = []
    # for _ in range(10):
    #     time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
    #
    # for dt in time:
    #     date_time = dt
    #     #user_id = random.randint(1, 10)
    #     #current_weight = random.randint(100,250)
    #     user_id = 1
    #     current_weight = 123

    date_time = datetime.datetime(2019, 2, 22, 19, 12, 22)
    current_weight = 123

    user_weight = Weight(current_weight=current_weight,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_weight)

    db.session.commit()


def load_glucose():
    """Load glucose over time."""

    print('Glucose')

    # time = []
    # for _ in range(10):
    #     time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
    #
    # for dt in time:
    #     date_time = dt
    #     #user_id = random.randint(1, 10)
    #     user_id = 1
    #     #current_glucose = random.randint(70, 125)
    #     current_glucose = 115

    date_time = datetime.datetime(2019, 1, 22, 19, 12, 22)
    current_glucose = 115

    user_glucose = Glucose(current_glucose=current_glucose,
                         date_time=date_time,
                         user_id=user_id,
                         )

    db.session.add(user_glucose)

    db.session.commit()

def load_glucose_two():
    """Load glucose over time."""

    print('Glucose')

    # time = []
    # for _ in range(10):
    #     time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
    #
    # for dt in time:
    #     date_time = dt
    #     # user_id = random.randint(1, 10)
    #     # current_glucose = random.randint(70, 125)
    #     user_id = 1
    #     current_glucose = 100

    date_time = datetime.datetime(2019, 2, 22, 19, 12, 22)
    current_glucose = 100

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
    load_glucose()
    load_glucose_two()

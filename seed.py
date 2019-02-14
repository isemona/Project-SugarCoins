"""Utility file to seed sugarcoins database from Faker Python"""


from sqlalchemy import func #  WHAT IS THIS??

# need to allow access to these Objects to load/seed data
from model import connect_to_db, db, Gender, User, Food, Sugar

# connecting to database aka SQL i.e. connect_to_db(app) has 'app' app comes from ther server so this needs to be imported too
from server import app

# to randomize on list of sweets and list of grams spent per day
# https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/, arguments is a range i.e. from 1 to 26
import random

# to use the datetime libary and syntax is datetime.datetime
import datetime 

# necessary imports to extract data from Faker library
from faker import Faker
from faker.providers import profile

fake = Faker()


sweets = ['snickers','soda','juice', 'M&Ms', 'yogurt', 'cereal']
alternative = ['stevia', 'orange', 'strawberry', 'blueberry', 'plum']
reason = ['tired', 'hangry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'experiencing-loss']
# notes would be different for woman - ['tired', 'hungry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'hormonal-related', 'experiencing-loss']

# keeping 'hormonal-related' out because this is past data




def load_users():
    '''Load users from Faker Library to database'''

    # print statement for testing
    print('Users') 


    # generating 10 user profile objects
    user_profiles = []
    for _ in range(10):
        user_profiles.append(fake.profile())
    
    # accessing properties in individual objects
    sugarholics = []
    for user in user_profiles:
        sugarholics.append([user['name'],user['sex']])


    for person in sugarholics:
        name = person[0]
        gender = person[1]

        user = User(name=name,
                gender_code=gender,
                )
        # We need to add to the session or it won't ever be stored
        db.session.add(user)
    

    # Once we're done, we should commit our work
    db.session.commit()

def load_gender():
    '''Load users from Faker Library to database'''

    # print statement for testing
    print('Gender') 

    female = Gender(gender_code='F',
                    allowance=25,
                    )

    male = Gender(gender_code='M',
                    allowance=25,
                    )

    
    db.session.add(female)
    db.session.add(male)

    db.session.commit()

def load_food():
    '''Load food from a list of sweets.'''

    # print statement for testing
    print('Food')


    food = random.choice(sweets)
    cost = random.randint(1,26) # FIX ME! Not sure how to differentiate between genders men should have 38g per day
    
    sweet_food = Food(food=food,
                cost=cost,
                )

    db.session.add(sweet_food)

    db.session.commit()


def load_sugar_intake():
    '''Load sugar intake at particular time and why.'''

    print('Sugar Intake')

    notes = random.choice(reason)

    time = []
    for _ in range(10):
        time.append(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))
    
    for dt in time:
        date_time = dt

        sugar_intake = Sugar(notes=notes,
                            date_time=date_time,
                            )

        db.session.add(sugar_intake)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    load_gender()
    load_users()
    load_food()
    load_sugar_intake()


"""Utility file to seed sugar_intake database from Faker Python"""

import datetime
from sqlalchemy import func
from model import connect_to_db, db
from server import app


import random
from faker import Faker
from faker.providers import profile

fake = Faker()


# User profile = faker.provider.profile
# Date time stamp = faker.provide.datetime
# Sugar quantity = faker.random (range 25g and 36g, male and female respectively)

# user_profiles = []
# for _ in range(10):
#     new.append(fake.profile())

# sugarholics = []
# for user in user_profiles:
#     sugarholics.append(i['name'] + " " + i['sex'] + " " + i['username'])


# random date and times
for _ in range(1):
    print(fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None))


food = ['snickers','soda','juice', 'M&Ms', ]

note_for_men = ['tired', 'hungry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'experiencing-loss']
note_for_women = ['tired', 'hungry', 'anxious', 'stressed', 'special event', 'peer-pressure', 'hormonal-related', 'experiencing-loss']
# keeping 'hormonal-related' out because this is past data

# https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/, arguments is a range i.e. from 1 to 26

sweet = random.choice(food)
cost_for_female = random.randint(1,26)
cost_for_male = random.randint(1,37)


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

    name = sugarholics[0]
    gender = sugarholics[1]

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

    female = Gender(gen_code='F',
                    allowance=25
                    )

    male = Gender(gen_code='M',
                    allowance=25
                    )

    # We need to add to the session or it won't ever be stored
    db.session.add(female)
    db.session.add(male)

    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()



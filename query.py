from builtins import len, int

from models import *

from sqlalchemy import cast, Date, func, extract
# from datetime import date
from datetime import datetime, timedelta


# init_app()

### Calculate the remaining sugar intake per day 25-total intake for women and 38-total intake for men

def get_user_list_of_food(session):
    """Info on list of foods and costs"""

    # todays_sugar is a list of objects
    # todays_sugar = db.session.query(Sugar).filter(cast(Sugar.date_time, Date) == date.today(),
    #                                               Sugar.user_id == session['user_id']).all()

    todays_sugar = db.session.query(Sugar).filter(cast(Sugar.date_time, Date) > datetime.utcnow() - timedelta(days=1),
                                                  Sugar.user_id == session['user_id']).all()
    list_of_foods = []

    for entry in todays_sugar:
        list_of_foods.append((entry.food.food_name, entry.food.cost))

    return list_of_foods

def get_lists_of_food(session):
    """Listing of food and price"""

    # todays_sugar is a list of objects
    todays_sugar = db.session.query(Sugar).filter(
        cast(Sugar.date_time, Date) > datetime.utcnow() - timedelta(days=1),
        Sugar.user_id == session['user_id']).all()

    foods = []
    for entry in todays_sugar:
        foods.append((entry.food.food_name + "__________________" + str(entry.food.cost)))

    return foods


def get_users(session):
    """Info on daily spending"""
    users = User.query.all()

    return users

def get_user(session):
    """Info on daily spending"""
    user = User.query.filter(User.user_id == session['user_id']).first()

    return user

def get_user_allowance(session):
    """Info on daily spending"""
    user = User.query.filter(User.user_id == session['user_id']).first()
    user_allowance = user.gender.allowance

    return user_allowance

def get_user_daily_spending(session):
    """Info on daily spending"""

    total = sum([cost for _, cost in get_user_list_of_food(session)])

    return total

def get_user_daily_balance(session):
    """Info on remaining"""

    if get_user_allowance(session) - total == negative:
        return 0
    else:
        return get_user_allowance(session) - total

def calculate_user_daily_spending_percentage(session):
    """Info on daily spending as a percentage"""

    daily_spending = get_user_daily_spending(session)

    return daily_spending / get_user_allowance(session) * 100


def get_monthly_spending(session):
    """Info on monthly spending"""

    user_monthly_info = (db.session.query(Sugar.user_id, extract('month', Sugar.date_time), func.sum(Food.cost))
                         .filter(Sugar.user_id == session['user_id'])
                         .join(Food).group_by(Sugar.user_id, extract('month', Sugar.date_time)).all())

    return user_monthly_info

def get_average_spending(session):
    """Info on average spending"""

    user_spending = (db.session.query(Sugar.user_id, extract('year', Sugar.date_time), func.sum(Food.cost))
                         .filter(Sugar.user_id == session['user_id'])
                         .join(Food).group_by(Sugar.user_id, extract('year', Sugar.date_time)).all())

    user_date_time = (db.session.query(Sugar.user_id, Sugar.date_time)
                    .filter(Sugar.user_id == session['user_id'])
                    .join(Food).group_by(Sugar.user_id, Sugar.date_time).all())

    dates = []

    for date in user_date_time:
        dates.append(date)

    spent = 0
    for item in user_spending:
        spent = item[2]

    # default value for new users
    if len(dates) == 0:
        return 0
    else:
        user_average = spent/len(dates)

    return int(user_average)

def get_user_notes(session):
    #user_sugar = db.session.query(Sugar).filter(Sugar.user_id == session['user_id']).all()
    todays_sugar = db.session.query(Sugar).filter(cast(Sugar.date_time, Date) > datetime.utcnow() - timedelta(days=1),
                                                  Sugar.user_id == session['user_id']).all()

    user_notes = [object.notes for object in todays_sugar]

    return user_notes

def get_user_moods(session):
    moods = get_user_notes(session)

    user_moods = {}
    for mood in moods:
        if mood not in user_moods:
            user_moods[mood] = 1
        else:
            user_moods[mood] += 1

    RESULTS = {'children': []}
    for item in user_moods:
        print(item)
        print(user_moods[item])
        RESULTS['children'].append({
            'name': item,
            'symbol': item,
            'price': user_moods[item],
            'net_change': 1,
            'percent_change': 1,
            'volume': 1,
            'value': user_moods[item]
        })

    return RESULTS

def get_user_weight(session):

    weekday = func.extract('isodow', Weight.date_time).label('weekday')

    user_monthly_weight = (db.session.query(Weight.user_id, extract('month', Weight.date_time), weekday, Weight.current_weight)
                           .filter(Weight.user_id == session['user_id'])
                           .join(User).group_by(Weight.user_id, extract('month', Weight.date_time), weekday, Weight.current_weight).all())

    return user_monthly_weight

def get_user_glucose(session):

    weekday = func.extract('isodow', Glucose.date_time).label('weekday')

    user_monthly_glucose = (db.session.query(Glucose.user_id, extract('month', Glucose.date_time), weekday, Glucose.current_glucose)
                           .filter(Glucose.user_id == session['user_id'])
                           .join(User).group_by(Glucose.user_id, extract('month', Glucose.date_time), weekday, Glucose.current_glucose).all())


    return user_monthly_glucose

def get_user_current_weight(session):
    user_weight_list = get_user_weight(session)

    current_weight = []
    for weight in user_weight_list:
        current_weight.append(weight.current_weight)

    # default value for new users
    if current_weight == []:
        return 0
    else:
        return current_weight[-1]

def get_user_current_glucose(session):
    glucose_list = get_user_glucose(session)

    current_glucose = []
    for level in glucose_list:
        current_glucose.append(level.current_glucose)

    # default value for new users
    if current_glucose == []:
        return 0
    else:
        return current_glucose[-1]



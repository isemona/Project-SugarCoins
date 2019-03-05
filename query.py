from model import *

from sqlalchemy import cast, Date, func, extract
from datetime import date


# init_app()

### Calculate the remaining sugar intake per day 25-total intake for women and 38-total intake for men

def get_user_list_of_food(session):
    """Info on list of foods and costs"""

    # todays_sugar is a list of objects
    todays_sugar = db.session.query(Sugar).filter(cast(Sugar.date_time, Date) == date.today(),
                                                  Sugar.user_id == session['user_id']).all()

    list_of_foods = []

    for entry in todays_sugar:
        list_of_foods.append((entry.food.food_name, entry.food.cost))

    return list_of_foods
    # for item in list_of_foods:
    #     return item


def get_user_allowance(session):
    """Info on daily spending"""
    user = User.query.filter(User.user_id == session['user_id']).first()
    user_allowance = user.gender.allowance

    return user_allowance


def get_user_daily_spending(session):
    """Info on daily spending"""

    total = sum([cost for _, cost in get_user_list_of_food(session)])

    return get_user_allowance(session) - total


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

    # new_list = []

    # for tup in new_list:
    #     return tup
    #     new_list.append(list(tup))

    return user_monthly_info


def get_user_notes(session):
    user_sugar = db.session.query(Sugar).filter(Sugar.user_id == session['user_id']).all()
    user_notes = [object.notes for object in user_sugar]

    return user_notes


def get_user_moods(session):
    moods = get_user_notes(session)

    # for mood in moods:
    #     if mood not in user_moods:
    #         user_moods[mood] = 1
    #     else:
    #         user_moods[mood] += 1

    # return user_moods

    user_moods = {}
    for mood in moods:
        if mood not in user_moods:
            user_moods[mood] = 1
        else:
            user_moods[mood] += 1

    RESULTS = {'children': []}
    for item in user_moods:
        RESULTS['children'].append({
            'name': item,
            'symbol': item,
            'price': 0,
            'net_change': 0,
            'percent_change': 0,
            'volume': 0,
            'value': user_moods[item]
        })

    return RESULTS


def get_user_weight(session):
    user_monthly_weight = (db.session.query(Weight.user_id, extract('month', Weight.date_time), Weight.current_weight)
                           .filter(Weight.user_id == session['user_id'])
                           .join(User).group_by(Weight.user_id, extract('month', Weight.date_time),
                                                Weight.current_weight).all())

    return user_monthly_weight


def get_user_glucose(session):
    glucose_list = db.session.query(Glucose).filter(Glucose.user_id == session["user_id"]).all()

    user_glucose = [user.current_glucose for user in glucose_list]

    return user_glucose

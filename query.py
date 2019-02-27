
from model import *

from sqlalchemy import cast, Date, func, extract
from datetime import date


#init_app()

### Calculate the remaining sugar intake per day 25-total intake for women and 38-total intake for men

def get_user_list_of_food(session):
    """Info on list of foods and costs"""

    # todays_sugar is a list of objects
    todays_sugar = db.session.query(Sugar).filter(cast(Sugar.date_time,Date) == date.today(),Sugar.user_id==session['user_id']).all()


    list_of_foods = []

    for entry  in todays_sugar:
        list_of_foods.append((entry.food.food_name, entry.food.cost))

    return list_of_foods
    # for item in list_of_foods:
    #     return item


def get_user_allowance(session):
    """Info on daily spending"""
    user = User.query.filter(User.user_id == session['user_id']).first()
    user_gender = user.gender
    user_allowance = user.gender.allowance

    return user_allowance


def get_user_daily_spending(session):
    """Info on daily spending"""

    total = sum([cost for _,cost in get_user_list_of_food(session)])

    return total - get_user_allowance(session)

def calculate_user_daily_spending_percentage(session):
    """Info on daily spending as a percentage"""

    daily_spending = get_user_daily_spending(session)

    return daily_spending/get_user_allowance(session)*100

def get_monthly_spending(session):
    """Info on monthly spending"""

    user_monthly_info = (db.session.query(Sugar.user_id, extract('month', Sugar.date_time), func.sum(Food.cost))
        .filter(Sugar.user_id == session['user_id'])
        .join(Food).group_by(Sugar.user_id, extract('month', Sugar.date_time)).all())

    #new_list = []

    # for tup in new_list:
    #     return tup
    #     new_list.append(list(tup))

    return user_monthly_info

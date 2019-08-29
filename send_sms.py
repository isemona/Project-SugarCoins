# Download the helper library from https://www.twilio.com/docs/python/install
from flask import session
from sqlalchemy import cast, Date, func, extract
from twilio.rest import Client
import schedule
import time
import os
import threading
from models import connect_to_db, db, User, Sugar
from query import get_users, get_user_daily_balance, get_phone_number
from sqlalchemy import cast, Date, func, extract
from datetime import datetime, timedelta

account_sid = os.environ.get('TWILIO_ACCOUNT_ID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_number = os.environ.get('MY_NUMBER')
twilio_number = os.environ.get('TWILIO_NUMBER')

# def send_msg():
#     user = get_user(session) # this changes everytime for each user so add it under the function
#     fullname = user.name
#     name_lst = fullname.split(' ')
#     firstname = name_lst[0]
#     balance = get_user_daily_balance(session) # this changes everytime for each user so add it under the function
#     phone_number = get_phone_number(session) # this changes everytime for each user so add it under the function
#     client = Client(account_sid, auth_token)
#     print(f"client.messages \\"
#           f"      .create("
#           f"           body='Hi {user}, you have {balance} coins left in your SugarWallet. Spend wisely!'"
#           f"           from_={twilio_number}"
#           f"           to={phone_number}"
#           f"       )")
#     message = client.messages \
#                     .create(
#                          body=f"Hi {firstname}, you have {balance} coins left in your SugarWallet. Spend wisely!",
#                          from_= twilio_number,
#                          to= phone_number #my_number # phone_number variable here
#                      )

#     print(message.sid)

def send_msg():
    users = User.query.filter(User.phone is not None)
    for user in users:
        firstname = user.name.split(' ',1) # guarantees that it will split it once
        user_allowance = user.gender.allowance
        todays_sugar = db.session.query(Sugar).filter(
            cast(Sugar.date_time, Date) > datetime.utcnow() - timedelta(days=1),
            Sugar.user_id == user.user_id).all()
        foods = []
        for entry in todays_sugar:
            foods.append((entry.food.food_name, entry.food.cost))
        total = sum([cost for _, cost in foods])
        balance = 0
        if user_allowance - total > 0:
            balance = user_allowance - total

        client = Client(account_sid, auth_token)
        # print(f"client.messages \\"
        #     f"      .create("
        #     f"           body='Hi {user}, you have {balance} coins left in your SugarWallet. Spend wisely!'"
        #     f"           from_={twilio_number}"
        #     f"           to={user.phone}"
        #     f"       )")
    
        message = client.messages \
                .create(
                        body=f"Hi {firstname}, you have {balance} coins left in your SugarWallet. Spend wisely!",
                        from_= twilio_number,
                        to= user.phone #my_number # phone_number variable here
                    )

if __name__ == "__main__":

    # only use when you are running send_sms_py
    # schedule.every(10).minutes.do(job)
    # schedule.every(2).seconds.do(send_msg)
    # schedule.run_continuously(1)
    # print("starting the program")
    send_msg()

    # The following code is used to test the schedule module ref: https://github.com/dbader/schedule
    # def job():
    #     print("I'm working...")

    # schedule.every(2).seconds.do(job)

    # cease_continuous_run = threading.Event()

    # class ScheduleThread(threading.Thread):
    #     @classmethod
    #     def run(cls):
    #         while not cease_continuous_run.is_set():
    #             schedule.run_pending()
    #             time.sleep(1)

    # continuous_thread = ScheduleThread()
    # continuous_thread.start()
    # print("Starting the Flask server")

    # within a file two things are done: import the code and run it, if we're running this file as a program run __main__
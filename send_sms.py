# Download the helper library from https://www.twilio.com/docs/python/install
from flask import session
from twilio.rest import Client
import schedule
import time
import os
from models import connect_to_db, db, User
from query import get_user, get_user_daily_balance, get_phone_number

account_sid = os.environ.get('TWILIO_ACCOUNT_ID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_number = os.environ.get('MY_NUMBER')
twilio_number = os.environ.get('TWILIO_NUMBER')

def send_msg():
    user = get_user(session) # this changes everytime for each user so add it under the function
    balance = get_user_daily_balance(session) # this changes everytime for each user so add it under the function
    phone_number = get_phone_number(session) # this changes everytime for each user so add it under the function
    # client = Client(account_sid, auth_token)
    print(f"client.messages \\"
          f"      .create("
          f"           body='Hi {user}, you have {balance} coins left in your SugarWallet. Spend wisely!'"
          f"           from_={twilio_number}"
          f"           to={phone_number}"
          f"       )")
    # message = client.messages \
    #                 .create(
    #                      body=f"Hi {user}, you have {balance} coins left in your SugarWallet. Spend wisely!",
    #                      from_= twilio_number,
    #                      to= phone_number #my_number # phone_number variable here
    #                  )

    # print(message.sid)
    # print(message)


if __name__ == "__main__":

    # only use when you are running send_sms_py
    # schedule.every(20).seconds.do(send_msg)
    # schedule.run_continuously(1)
    print("starting the program")
    send_msg()

# within a file two things are done: import the code and run it, if we're running this file as a program run __main__
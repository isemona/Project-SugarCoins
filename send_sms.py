# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import schedule
import time
import os
#from model import connect_to_db, db, User
#from query import *


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_number = os.getenv('MY_NUMBER')
twilio_number = os.getenv('TWILIO_NUMBER')

def send_msg():

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=f"You have 8 coins left in your SugarWallet. Spend wisely! ",
                         from_= twilio_number,
                         to= my_number # phone_number variable here
                     )

    print(message.sid)

# def send_msg():
#
#     users = get_users(session)
#     remaining = get_user_daily_balance(session)
#
#     for user in users:
#         phone_number = user.phone
#         # Your Account Sid and Auth Token from twilio.com/console
#         account_sid = process.secrets.sh.TWILIO_ACCOUNT_ID;
#         auth_token = process.secrets.sh.TWILIO_AUTH_TOKEN;
#
#         client = Client(account_sid, auth_token)
#
#         message = client.messages \
#                         .create(
#                              body=f"You have {remaining} coins left in your SugarWallet. Spend wisely! ",
#                              from_='+14244003773',
#                              to='+14084124657' # phone_number variable here
#                          )
#
#         print(message.sid)

def job():


    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("12:00").do(send_msg)
    # schedule.every(5).to(10).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)
    schedule.every(20).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)



if __name__ == "__main__":

    schedule.run_continuously(1)
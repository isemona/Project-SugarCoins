# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import schedule
import time
import os
#from model import connect_to_db, db, User
#from query import *


account_sid = os.environ.get('TWILIO_ACCOUNT_ID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_number = os.environ.get('MY_NUMBER')
twilio_number = os.environ.get('TWILIO_NUMBER')

def send_msg():

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        # body=f"Hi {{}}, you have 8 coins left in your SugarWallet. Spend wisely! ",
                         body=f"Hi Semona, you have 8 coins left in your SugarWallet. Spend wisely!",
                         from_= twilio_number,
                         to= "+17876462316" #my_number # phone_number variable here
                     )

    print(message.sid)



if __name__ == "__main__":

    # only use when you are running send_sms_py
    schedule.every(20).seconds.do(send_msg)
    schedule.run_continuously(1)
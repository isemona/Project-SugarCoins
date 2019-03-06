# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import schedule
import time
from model import connect_to_db, db, User
from query import get_user_daily_balance(session) as remaining get_users(session) as users


def send_msg():

    for user in users:
        phone_number = user.phone
        # Your Account Sid and Auth Token from twilio.com/console

        account_sid = 'AC8c90676a4ed1ff99e843ad9bfe5139d5'
        auth_token = 'edf191b3c972e3ed941a7270d83956ef'
        client = Client(account_sid, auth_token)



        message = client.messages \
                        .create(
                             body=f"You have {remaining} coins left in your SugarWallet. Spend wisely! ",
                             from_='+14244003773',
                             to='+14084124657' # phone_number variable here
                         )

        print(message.sid)

def job():


    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    schedule.every().day.at("12:00").do(send_msg)
    # schedule.every(5).to(10).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)



if __name__ == "__main__":

    schedule.run_continuously(1)
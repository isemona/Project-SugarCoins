# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC8c90676a4ed1ff99e843ad9bfe5139d5'
auth_token = 'edf191b3c972e3ed941a7270d83956ef'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+14244003773',
                     to='+14084124657'
                 )

print(message.sid)
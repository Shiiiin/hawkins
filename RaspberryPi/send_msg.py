from twilio.rest import Client
from config import *  # config.py module

def send_message():
    account_sid = ACCOUNT_SID  # Put your Twilio account SID here
    auth_token = AUTH_TOKEN  # Put your auth token here
    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(
        to=TO,  # Put your cellphone number here
        from_=FROM,  # Put your Twilio number here
        body="This is a text send from Raspberry Pi.")

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone = os.environ['TWILIO_PHONE_NUM']
my_phone = os.environ['MY_PHONE_NUM']
mer_phone = my_phone = os.environ['MER_PHONE_NUM']

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body = "I'm sorry Dave, I'm afraid I can't do that",
                     from_= twilio_phone,
                     to = my_phone
                 )

message = client.messages \
                .create(
                     body = "I'm sorry Dave, I'm afraid I can't do that",
                     from_= twilio_phone,
                     to = mer_phone
                 )

print(message.sid)

# can check other things like
message.status
message.date_sent

# alternative... send email like:
# 5551234567@vtext.com for verizon.. this is free..
import os
from twilio.rest import Client

# # Read text from the credentials file and store in data variable
# with open('credentials.txt', 'r') as myfile:
#   data = myfile.read()
#
# # Convert data variable into dictionary
# info_dict = eval(data)
#
# # Your Account SID from twilio.com/console
# account_sid = info_dict['account_sid']
#
# # Your Auth Token from twilio.com/console
# auth_token = info_dict['auth_token']
#
# # Set client and send the message
# client = Client(account_sid, auth_token)
# message = client.messages.create( to =info_dict['your_num'], from_ = info_dict['trial_num'], body= "What's Up Man")



acc_sid = "AC681de6ab7d530957adda1aef79ffcce3"
acc_token = "1b6ec89c81014ce2160ad985dab28d4d"

clint = Client(acc_sid, acc_token)

sms = clint.messages.create(
    from_="+19285636626",
    body="Hello, from FBI",
    to="+977 986-2230210",

)

print(sms.sid)

# VoteTextBot

A text bot that provides election information based on a given zip code.


## Initial setup (MacOS)
+ Get python (nothing additional to run) and twilio (`pip install twilio` or `easy_install twilio`)
+ Get virtualenv (`pip install virtualenv`)
+ Get ngrok (from https://ngrok.com/download)
+ Update node (`sudo n stable`) and get the twilio CLI tools `npm install twilio-cli -g`
+ Set Twilio environment variables:
```
export TWILIO_ACCOUNT_SID=ACb0ddafbfd39216658f9e25f5924cb067
export TWILIO_AUTH_TOKEN=877811963def53468433bd66b43d2bb8
```
+ Activate virtualenv and get dependencies
```
cd VoteTextBot
virtualenv --no-site-packages .
source bin/activate
bin/pip install -r requirements.txt
```
## Run program:
+ Run file (`python process_text.py`)
+ Run following in a different terminal window: `twilio phone-numbers:update "+13342581763" --sms-url="http://localhost:5000/"`
+ Bot is active! Begin the conversation with "Hello" (capitalization doesn't matter, but the message can only contain that one word).

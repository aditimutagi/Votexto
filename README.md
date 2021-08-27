# VoteTextBot

A text bot that provides election information based on a given zip code (for now, test with 11050).


## UPDATE: 08/27/2021
	Free trial of Twilio has expired. New authentication ID (Account SID: ACa41a4e93b1085edbf3220ff24a52b8eb), token (3b2f440c4e1146e764c4ef71671f28e3), and phone number (+12678438180) needed to run the code. 

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
Python files are not linked together, run independently of each other as of now

* Run file (`python process_text.py`)
	+ Run following in a different terminal window: `twilio phone-numbers:update "+13342581763" --sms-url="http://localhost:5000/"`
	+ Bot is active! Begin the conversation with "Hello" (capitalization doesn't matter, but the message can only contain that one word).

* Run file ('CandidatePlatformInformation.py')
	+ Uses webscraping to retrieve platform information from https://www.ontheissues.org/default.htm
	+ Currently includes information on Democratic and Republican presidential candidates
	+ This algorithm can be applied to retreive non-partisan platform information for presidential, congress, and state elections

* Run file ('PollingLocations.py')
	+ Uses webscraping of https://voterlookup.elections.ny.gov to automate process of finding polling locations
	+ Allows users to input details requested in form, prints nearest polling location
	+ Currently finds polling locations for New York, can be implemented to other state-specific voting sites

* Run file ('VotingRegistration.py')
	+ Uses webscraping of https://voterreg.dmv.ny.gov/MotorVoter/ to automate voter registration 
	+ Allows users to input details requested in form, prints confirmation of registration
	+ Currently allows user to register to vote in New York, can be implemented to other state-specific voting registration sites
	
* Run file ('CovidFeedback.py')
	+ Uses user input to estimate risk faced by community members going to the same location throughout the day
	+ Users are prompted to answer a survey about COVID-related risks and safety measures at their polling locations
	+ These responses will be taken into account to suggest safer polling locations and an estimated waittime for other community members

from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import csv

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# dictionary containing all the info from the .csv -- 
zip_to_info_dict = {"U.S." : ["upcoming_elections", "senate_races", "house_races", "local_races"]}

# read the database.csv file
def readCSV():
    with open('info.csv', 'rU') as file:
        rdr = csv.reader(file, delimiter=',')
        line_count = 0
        for row in rdr:
            if line_count != 0:
                temp = ["", "", "",""]
                for i in range(4):
                    temp_str = row[i+1].decode('utf-8')
                    temp[i] = temp_str.replace("{xe", "\n")
                    #print temp[i]
                zip_to_info_dict[row[0]] = [temp[0],temp[1],temp[2],temp[3]]
            line_count += 1

# zip is a string, num is an int
def getDataWithContextString(zip, num):
    result = "Not Found"
    if zip in zip_to_info_dict:
        result = zip_to_info_dict[zip][num-1]
    return result

@app.route("/", methods=['GET', 'POST'])
def processText():
    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1
    readCSV()
    # Save the new counter value in the session
    session['counter'] = counter
    # Build our reply
    message = ""
    if request.values.get('Body').lower() == "hello":
        # the response to the first hello message.
        message = "Hi!\nFor area-specific information, please input a zip code. Otherwise, please reply with '0'."
        session['last_hello'] = counter
    elif counter == (session['last_hello'] + 1):
        # the response to the zip code message
        message = "Thanks!\nReply '1' for upcoming election details.\nReply '2' for house races.\nReply '3' for senate races.\nReply '4' for local races.\nReply '5' for testing resources."
        try:
            temp_zip = int(request.values.get('Body'))
            # TODO: add input sanitization for the zip code.
            if temp_zip == 0:
                session['zip'] = "U.S."
            else:
                session['zip'] = request.values.get('Body')
        except ValueError:
            session['zip'] = "U.S."
    else:
        # all other messages
        try:
            num = int(request.values.get('Body'))
            zip_str = session['zip']
            message = getDataWithContextString(zip_str, num)
        except ValueError:
            message = "Sorry, that is not a valid option."

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import csv

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# dictionary containing all the info from the .csv -- UNFINISHED NEEDS TO BE UPDATED
zip_to_info_dict = {"U.S." : ["N/A", "Presidential election: Nov 3rd, 2020", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]}

# dictionary for biden,trump,harris,pence -- UNFINISHED, needs to be updated
national_platforms = {"B":["Improve the economy", "affordable care act", "don't defund the police"], 
    "T":["Improve the economy", "affordable care act", "don't defund the police"], 
    "H":["Improve the economy", "affordable care act", "don't defund the police"],
    "P":["Improve the economy", "affordable care act", "don't defund the police"]}

# this variable tracks the conversation, the first element will be the main menu level selection
previous_selections = []

# read the database.csv file
def readCSV():
    global zip_to_info_dict
    with open('info.csv', 'rU') as file:
        rdr = csv.reader(file, delimiter=',')
        line_count = 0
        for row in rdr:
            if line_count != 0:
                temp = ["", "", "","","", "", "","","", ""]
                for i in range(2):
                    temp_str = row[i+1] #.decode('utf-8')
                    temp[i] = temp_str.replace("{xe", "\n")
                    #print temp[i]
                zip_to_info_dict[row[0]] = [temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9],temp[10]]
            line_count = line_count + 1

def handleOptions(zip, num):
    global previous_selections
    # This means this is the first level, main menu level
    if not previous_selections:
        previous_selections.append(num)
        if num == "1":
            return howToRegister(zip)
        elif num == "2":
            return getElectionTimeline(zip)
        elif num == "3":
            return getPollingPlace(zip)
        elif num == "4":
            return getAbsenteeInfo(zip)
        elif num == "5":
            return getCandidatesPlatform(zip)
    elif len(previous_selections)==1: #second level
        previous_level = int(previous_selections[0])
        if previous_level==1: #how do i register sub-menu
            if num == "1":
                previous_selections.append(num)
                return "You must be:\nA U.S. citizen.\n18 years old on or before Election Day\nRegistered to vote by your state's voter registration deadline.\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == "2":
                previous_selections.append(num)
                return getDataWithContextString(zip,1) + "\nReply 'b' to go back.\nReply 'h' to go to the main menu." #1 is for the index of the column from csv file, which is website
            if num == 'b' or num == 'h':
                previous_selections.pop()
                return getMainMenu()
        elif previous_level==2: # election timeline submenu
            if num == "1":
                previous_selections.append(num)
                return "Upcoming elections: " + getDataWithContextString(zip,2) + "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == 'b' or num == 'h':
                previous_selections.pop()
                return getMainMenu()
        elif previous_level==3: #polling place
            if num == "1":
                previous_selections.append(num)
                return getDataWithContextString(zip, 4)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == 'b' or num == 'h':
                previous_selections.pop()
                return getMainMenu()
        elif previous_level ==4: # absentee info
            if num == "1":
                previous_selections.append(num)
                return getDataWithContextString(zip, 5)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            elif num == "2":
                previous_selections.append(num)
                return getDataWithContextString(zip, 6)+"\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == 'b' or num == 'h':
                previous_selections.pop()
                return getMainMenu()
        elif previous_level== 5: # candidate platform
            if num == "1":
                previous_selections.append(num)
                return presidential()
            if num =="2":
                previous_selections.append(num)
                return vicePresidential()
            if num =="3":
                previous_selections.append(num)
                return congressional(zip)
            if num =="4":
                previous_selections.append(num)
                return local(zip)
    elif len(previous_selections)==2: #third level
        mainMenuItem = int(previous_selections[0])
        secondLevelItem = int(previous_selections[1])
        # Only options 5 reach this layer
        if mainMenuItem==5:
            if secondLevelItem == 1: # presidential
                if num == "1" or num == "2": # platform of biden or trump
                    previous_selections.append(num)
                    return platformMenu()
                if num == 'b':
                    previous_selections.pop()
                    return presidential()
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
            if secondLevelItem == 2: # vice presidential
                if num == "1" or num == "2": # platform of harris or pence
                    previous_selections.append(num)
                    return platformMenu()
                if num == 'b':
                    previous_selections.pop()
                    return vicePresidential()
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
            if secondLevelItem == 3: # congressional
                if num == "1": # house of reps
                    previous_selections.append(num)
                    return "Your house of representative candidates are:" + getDataWithContextString(zip, 9)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == "2": # senators
                    previous_selections.append(num)
                    return "Your senate candidates are:" + getDataWithContextString(zip, 9)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == 'b':
                    previous_selections.pop()
                    return congressional(zip)
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
            if secondLevelItem == 4: # local
                if num == "1":
                    previous_selections.append(num)
                    return ". \nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == 'b':
                    previous_selections.pop()
                    return local(zip)
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
    elif len(previous_selections) == 3: #fourth level, only valid for the 5th option
        secondLevelItem = int(previous_selections[1])
        thirdLevelItem = int(previous_selections[2])
        # Only option 5 reach this layer
        if secondLevelItem == 1: # presidential
            who = "" #biden or trump
            if thirdLevelItem == 1:
                who = "B"
            else:
                who = "T"
            if num == "1":
                previous_selections.append(num)
                return national_platforms[who][0]
            if num == "2":
                previous_selections.append(num)
                return national_platforms[who][1]
            if num == "3":
                previous_selections.append(num)
                return national_platforms[who][2]
            if num == 'b':
                previous_selections.pop()
                return platformMenu()
            if num == 'h':
                previous_selections = []
                return getMainMenu()
        if secondLevelItem == 2: # vice presidential
            who = "" #harris or pence
            if thirdLevelItem == 1:
                who = "H"
            else:
                who = "P"
            if num == "1":
                previous_selections.append(num)
                return national_platforms[who][0]
            if num == "2":
                previous_selections.append(num)
                return national_platforms[who][1]
            if num == "3":
                previous_selections.append(num)
                return national_platforms[who][2]
            if num == 'b':
                previous_selections.pop()
                return platformMenu()
            if num == 'h':
                previous_selections = []
                return getMainMenu()
        if secondLevelItem == 3: # congressional and local todo -- UNFINISHED
            if num == "1": # house of reps
                previous_selections.append(num)
                return "Your house of representative candidates are:" + getDataWithContextString(zip, )+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == "2": # senators
                previous_selections.append(num)
                return ". \nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == 'b':
                previous_selections.pop()
                return congressional(zip)
            if num == 'h':
                previous_selections = []
                return getMainMenu()
        if secondLevelItem == 4: # local -- UNFINISHED
            if num == "1": # house of reps
                previous_selections.append(num)
                return ". \nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == "2": # senators
                previous_selections.append(num)
                return ". \nReply 'b' to go back.\nReply 'h' to go to the main menu."
            if num == 'b':
                previous_selections.pop()
                return local(zip)
            if num == 'h':
                previous_selections = []
                return getMainMenu()
    return "Invalid option."

# the following functions are for option 5
def platformMenu():
    return "Reply '1' for economy.\nReply '2' for healthcare.\nReply '3' for police.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

def presidential():
    return "Here are your 2020 Presidential candidates:\nJoe Biden (D)\nDonald Trump (R)\nReply '1' for Joe Biden's platforms.\nReply '2' for Donald Trump's platforms.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

def vicePresidential():
    return "Here are your 2020 Vice Presidential candidates:\nKamala Harris (D)\nMike Pence (R)\nReply '1' for Kamala Harris's platforms.\nReply '2' for Mike Pence's platforms.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

def congressional(zip):
    return "Here are your 2020 Congressional candidates:" + getDataWithContextString(zip, 7)+"\n" #TODO finish this

def local(zip):
    return "Here are your local candidates:" + getDataWithContextString(zip, 8)+"\n" #TODO finish this

def getMainMenu():
    return "Reply '1' for information on how to register.\nReply '2' for election timeline and deadlines.\nReply '3' to find your polling place.\nReply '4' for absentee / mail-in ballot information.\nReply '5' to find out who's on your ballot."


# This is option 1 in the main menu
def howToRegister(zip):
    if zip == 0:
        return "Reply '1' for U.S. voting registration requirements.\nReply '2' for general registration instructions.\nReply 'b' to go back.\nReply 'h' to go to the main menu."
    else:
        return "Reply '1' for U.S. voting registration requirements.\nReply '2' for your state's voting website.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

# This is option 2 in the main menu
def getElectionTimeline(zip):
    if zip == 0:
        return "The general election will be on November 3, 2020. Sorry, other dates and deadlines require your zip code. \nReply 'b' to go back.\nReply 'h' to go to the main menu."
    else:
        return "Reply '1' for upcoming election dates and registration deadlines.\nReply '2' for deadlines for mail-in ballots.\nReply '3' for early voting dates.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

# This is option 3 in the main menu
def getPollingPlace(zip):
    if zip == 0:
        return "Sorry, finding your polling place requires your zip code.\nReply 'b' to go back.\nReply 'h' to go to the main menu."
    else:
        return getDataWithContextString(zip, 3)+"\nReply '1' for COVID-19 related policies at your polling place.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

# This is option 4 in the main menu
def getAbsenteeInfo(zip):
    if zip == 0:
        return "Sorry, finding absentee info depends on your zip code.\nReply 'b' to go back.\nReply 'h' to go to the main menu."
    else:
        return "Reply '1' for your state's absentee voting policy.\nReply '2' for deadlines for mail-in ballots.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

# This is option 5 in the main menu
def getCandidatesPlatform(zip):
    if zip == 0:
        return "Reply '1' for U.S. Presidential candidates and platforms.\nReply '2' for U.S. Vice Presidential candidates and platforms.\nReply 'b' to go back.\nReply 'h' to go to the main menu."
    else:
        return "Reply '1' for U.S. Presidential candidates and platforms.\nReply '2' for U.S. Vice Presidential candidates and platforms.\nReply '3' for Congressional candidates and platforms.\nReply '4' for Local representative candidates and platforms.\nReply 'b' to go back.\nReply 'h' to go to the main menu."


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
        message = "Hi!\n Welcome to Robovote!\nFor area-specific information, please input a zip code. Otherwise, please reply with '0'."
        session['last_hello'] = counter
    elif counter == (session['last_hello'] + 1):
        # the response to the zip code message
        message = "Thanks!\n" + getMainMenu()
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
            optionSelected = request.values.get('Body')
            zip_str = session['zip']
            message = handleOptions(zip_str, optionSelected)
            print(previous_selections)
        except ValueError:
            message = "Sorry, that is not a valid option."

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

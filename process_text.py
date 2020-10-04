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
#XXX Add more list items for each of the 4 people
national_platforms = {"B":["""This summer, Mr. Biden rolled out his own set of economic proposals under the slogan 'Build Back Better,' 
including plans to invest in clean energy and to ensure that procurement spending goes toward American-made products. Mr. Biden is calling for tax increases on corporations and high-earning individuals, but he has said that no one earningless than $400,000 would face a tax hike.""", """Mr. Biden spent 36 years as a senator and eight years as vice president, 
so he has a voluminous record — giving him achievements to brag about, but also leaving him vulnerable over other aspects of 
his lengthy career.\nMr. Biden can point to accomplishments like the passage of the Violence Against Women Act, as well as 
the enactment of the Affordable Care Act and his work on the implementation of the 2009 stimulus package.\nMr. Trump has portrayed 
Mr. Biden’s record in a very different light, and Mr. Biden has faced criticism over a number of votes during the 2020 campaign, 
including his support for the Iraq war, the 1994 crime bill and NAFTA.""", """Mr. Biden has put a major focus on the virus, 
condemning Mr. Trump’s handling of the pandemic and making that a central argument as he asks voters to deny the 
president a second term. That is almost certain to be a major focus of Mr. Biden’s in the debate, too. 
He has promised a starkly different approach to combating the virus, stressing the importance of deferring to scientific experts,
and he has called for a national mask mandate.""",
"""Mr. Biden has pledged to nominate a Black woman to the Supreme Court, though he has declined to follow Mr. Trump’s lead and release a 
list of potential nominees. He has called for Senate Republicans to hold off on confirming a successor to Justice Ruth Bader Ginsburg 
until after the election, noting that early voting is already underway.""",
"""Mr. Biden has repeatedly said that he opposes defunding the police, though Republicans have still falsely claimed that he supports that movement. 
He has condemned violence as well. Mr. Biden has called for racial healing and pledged to confront systemic racism, a starkly different approach from 
Mr. Trump’s. In July, Mr. Biden released a plan to address racial inequities in the economy. 
\nMr. Biden’s message ties back to the origin of his campaign and themes of American values, as he often talks about being motivated to 
run by Mr. Trump’s comments after the white supremacist rally in Charlottesville, Va., in 2017.""",
"""Mr. Biden has warned that Mr. Trump is seeking to undermine the legitimacy of the election. 
"This president is going to try to indirectly steal the election by arguing that mail-in ballots don’t work,” he said in July.
\nMr. Biden has also warned about possible foreign interference, vowing that as president, he would impose significant consequences 
for any meddling by foreign powers. Last week, he called Mr. Trump’s refusal to commit to a peaceful transfer of power a 'typical 
Trump distraction.'"""], 
    "T":["""Until the pandemic, one of Mr. Trump’s strongest arguments for re-election was the powerful performance of the economy, 
which had achieved low unemployment, strong growth and a soaring stock market. Following the virus-induced shutdowns, the economy’s growth has stalled and unemployment has soared, even with some recovery in recent months. On the campaign trail, Mr. Trump promises 
that the economy will recover — and get even better — if he is given a second term. The president has also promised a future tax cut 
for the middle class, though he has not offered specifics, and he has said he wants to reduce the capital gains tax.""", 
    """At his campaign rallies, the president focuses on trade, including his renegotiation of the North American Free Trade Agreement, or NAFTA, 
and imposition of tariffs on China and other countries. He boasts about his 2017 tax cuts and the growth in jobs before the coronavirus pandemic. 
He cites increases in military funding, his elimination of environmental regulations, peace agreements in the Middle East and actions to shut down 
immigration.\nMany of the president’s promises fell short, a point that Mr. Biden may highlight. Despite saying he would build a “big, beautiful 
wall” across the entire border with Mexico, the president has built only about 200 miles of wall, most of it replacements for existing barriers. 
He failed to repeal the Affordable Care Act, and he has not controlled federal spending.\nIn addition to Mr. Trump’s record in the White House, 
another issue likely to come up is his taxes. Mr. Trump has refused to release his tax returns, and The New York Times reported on Sunday that he 
paid only $750 in federal income taxes in 2016 and in 2017.""", """Mr. Trump has repeatedly claimed that his administration’s response to the coronavirus 
pandemic was exceptional, saying he acted early to impose travel restrictions from China; worked with states to acquire equipment like ventilators; and 
pushed for the development of treatments and vaccines. Note, however, that the president consistently played down the threat from the virus in the early days 
when it could have been contained, and ignored or resisted advice from his top health officials. The United States failed to provide enough testing 
to know how the virus was spreading, and Mr. Trump clashed with governors over the need for protective equipment. There is also mounting evidence 
of the ways in which Mr. Trump and the White House put immense political pressure on the Centers for Disease Control and Prevention and other health 
agencies to accept Mr. Trump’s demands that the country reopen more quickly than they thought was safe.""","""The intense push to seat Judge Amy Coney Barrett 
on the Supreme Court before Election Day is part of the president’s four-year effort to remake the federal judiciary, adding conservative-leaning judges 
to the bench at all levels. With the help of a Republican-controlled Senate, Mr. Trump is succeeding in that goal.\nThe president has already installed two other Supreme 
Court justices — Neil M. Gorsuch and Brett M. Kavanaugh — and more than 200 federal district and appeals court judges, shifting the ideological balance 
for years to come.""","""The president has seized upon unrest over racial justice as a defining difference between him and Mr. Biden, 
calling the protesters “rioters” and “anarchists” and overtly siding with the police in a bid to cast himself as a “law and order” leader.\nThe president 
and his campaign are using episodes of violence against the police to generate fear and support among his base. He has called for much more aggressive 
use of the National Guard to control disturbances, and has dismissed the Black Lives Matter organization as a radical, violent group.\nWhen he is pressed 
for accomplishments, Mr. Trump cites the First Step Act, which made some reforms to federal sentencing laws, benefiting minorities. The bipartisan bill 
passed in 2018 and was signed into law by Mr. Trump.\nMr. Trump has attacked Mr. Biden as anti-law enforcement, often in exaggerated terms — though at 
times the president has also tried to cast him as overly punitive because of his work on the 1994 crime bill that encouraged incarceration.""","""Mr. Trump has 
spent much of the last year overtly questioning the integrity of the coming election, laying the groundwork for a legal and public relations 
assault if the initial count shows that he has lost the race.\nThe president’s primary focus in the past several months has been on mail-in ballots, 
which he claims — without any evidence — are subject to widespread fraud and should not be allowed."""], 
    "H":["See Joe Biden's Platforms.", "See Joe Biden's Platforms.", "See Joe Biden's Platforms.","See Joe Biden's Platforms.","See Joe Biden's Platforms.","See Joe Biden's Platforms."],
    "P":["See Donald Trump's Platforms.", "See Donald Trump's Platforms.", "See Donald Trump's Platforms.","See Donald Trump's Platforms.","See Donald Trump's Platforms.","See Donald Trump's Platforms."]}

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
                for i in range(10):
                    temp_str = row[i+1]#.decode('utf-8')
                    temp[i] = temp_str.replace("{xe", "\n")
                    temp[i] = temp[i].replace("{xy", ",")
                zip_to_info_dict[row[0]] = [temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9]]#had temp[10]
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
        if mainMenuItem==1:
            if secondLevelItem == 1: # how to register
                if num == 'b': # TODO fix
                    previous_selections.pop()
                    return getDataWithContextString(zip, 4)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
        elif mainMenuItem==2:
            if secondLevelItem == 1: # election timeline
                if num == 'b':
                    previous_selections.pop()
                return "Upcoming elections: " + getDataWithContextString(zip,2) + "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
        elif mainMenuItem==3:
            if secondLevelItem == 1: # polling place
                if num == '1':
                    previous_selections.append('1')
                    return "COVID-19 policies:"
                if num == 'b':
                    previous_selections.pop()
                    return getDataWithContextString(zip, 4)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                if num == 'h':
                    previous_selections = []
                    return getMainMenu()
        elif mainMenuItem==4: # absentee/mailin -- does this work??
            if num == 'b':
                previous_selections.pop()
                if secondLevelItem ==1:
                    return getDataWithContextString(zip, 5)+ "\nReply 'b' to go back.\nReply 'h' to go to the main menu."
                elif secondLevelItem ==2:
                    return getDataWithContextString(zip, 6)+"\nReply 'b' to go back.\nReply 'h' to go to the main menu."
            elif num == 'h':
                previous_selections = []
                return getMainMenu()
        elif mainMenuItem==5:
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
                return national_platforms[who][2] #XXX Add more if num == 4 etc. etc.
            if num == "4":
                previous_selections.append(num)
                return national_platforms[who][3]
            if num == "5":
                previous_selections.append(num)
                return national_platforms[who][4]
            if num == "6":
                previous_selections.append(num)
                return national_platforms[who][5]
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
    #XXX Add more items here -- all the related changes should have a comment w XXX
    return "Reply '1' for Economy.\nReply '2' for Trump’s and Biden’s records\nReply '3' for Coronavirus.\nReply '4' for Supreme Court.\nReply '5' for Race and violence in American cities\nReply '6' for Integrity of Elections.\nReply 'b' to go back.\nReply 'h' to go to the main menu."

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
    global previous_selections
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
        message = "Hi! Welcome to Votexto!\nFor area-specific information, please input a zip code. Otherwise, please reply with '0'."
        session['last_hello'] = counter
        previous_selections = []
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
            print(previous_selections)
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

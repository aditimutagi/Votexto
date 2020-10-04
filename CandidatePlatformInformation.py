#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 23:55:34 2020

@author: aditimutagi
"""

import requests
from bs4 import BeautifulSoup
import urllib

president = input("Which presidential candidate would you like to learn more about?\n")

if (president == "Trump"):
    URL = "https://www.ontheissues.org/Donald_Trump.htm"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Top issues: foriegn policy, gun control, economy, abortion\n")
    #will be scraped in future- currently copied from site
    print("Abortion: Ban the late-term abortion of babies. (Feb 2020), End medical research that uses tissue from aborted fetuses. (Jun 2019), FactCheck: Late abortions only for non-viable fetus. (Feb 2019)\n")
    print("Foreign Policy: We rebuilt military; America stronger than ever. (Feb 2020), Protect human rights in Hong Kong against China. (Nov 2019), Postpone meeting with Denmark if no Greenland discussion. (Aug 2019)\n")
    print("Economy: When stocks go up, everyone does well, not just the wealthy. (Sep 2020), AdWatch: market crash due to lack of coronavirus action. (Mar 2020), OpEd: Trump should take responsibility for corona panic. (Mar 2020)\n")
    print("Gun Control: Remove weapons from dangerous individuals, not all Americans. (Mar 2018), Arm public school employees to prevent school shootings. (Mar 2018), Opposes arming school teachers against school shootings. (Mar 2018)\n")
elif (president == "Biden"):
    URL = "https://www.ontheissues.org/Joe_Biden.htm"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Top issues: foriegn policy, gun control, economy, abortion\n")
    #will be scraped in future- currently copied from site
    print("Abortion: Fact-Check: opposes Hyde Amendment, after decades of support. (Jul 2019), Unequivocal support for abortion rights; Congress must act. (Jul 2019), I accept church rule personally, but not in public life. (Oct 2012)\n")
    print("Foreign Policy: The days of cozying up to dictators is over. (Aug 2020), Meet with North Korea and China together. (Feb 2020), Helped with $750M Latin America funding. (Feb 2020)\n")
    print("Economy: We will rebuild economy & build it back better. (Aug 2020), Ordinary people are getting killed by this economy. (Feb 2020), I got GOP Senators to vote for stimulus & other funding. (Jun 2019)\n")
    print("Gun Control: I go skeet-shooting, badly, and my sons go bird-hunting. (Feb 2020), I pushed Brady Bill when other Dems voted against it. (Feb 2020), I beat the NRA twice: AR-15s & high-capacity magazines. (Oct 2019)\n")



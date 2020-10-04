#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 12:27:00 2020

@author: aditimutagi
"""

covidFeedback = input("Congratulations on successfully voting! We hope that Votexto helped you make an informed decision and plan your Election Day! To better serve others within your community, we would greatly appreciate feedback regarding COVID-19 related risks and safety measures at your polling location. Enter Y to continue with a short survey.\n")

if (covidFeedback == 'Y'):
    #these variables will be used to estimate risk at each polling location over time and make recommendations accordingly
    crowdedness = input("Wonderful! To the best of your judgement, how crowded was your polling location? Please enter L for low crowdedness, M for moderate, and H for high\n")
    sd = input("Were social distancing measures strictly regulated and followed? Y or N\n")
    masks = input("To what extent were masks worn regularly and properly (that being, covering the nose and mouth)? Please enter L for low mask usage, M for moderate, and H for high\n")
    santization = input("Were places and objects of common contact sanitized after each use? Y or N\n")
    wait = input("About how long was your wattime?\n")
    
print("Thank you for using Votexto! We greatly appreciate your responses as it will help us better inform other members of your community during this Election Day! We hope to see you at the polls during the next election!\n")

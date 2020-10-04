#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 00:51:07 2020

@author: aditimutagi
"""

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin

session = HTMLSession()

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


url = "https://voterlookup.elections.ny.gov"
# get all form tags
forms = get_all_forms(url)
# iteratte over forms
for i, form in enumerate(forms, start=1):
    form_details = get_form_details(form)
    #print("="*50, f"form #{i}", "="*50)
    #print(form_details)
    
    
first_form = get_all_forms(url)[0]
#print(first_form)
county = input("What county do you reside in?\n")
form_details = get_form_details(first_form)
data = {}

form_details = get_form_details(first_form)
data = {}
for input_tag in form_details["inputs"]:
    if input_tag["name"] == "SelectedCountyId":
        # if it's hidden, use the default value
        #county = input(f"{input_tag['name']}: ")
        data[input_tag["name"]] = input_tag[county]
    elif input_tag["type"] == "hidden":
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit" and input_tag["name"]!= "g-recaptcha-response":
        # all others except submit, prompt the user to set it
        value = input(f"{input_tag['name']}: ")
        data[input_tag["name"]] = value
   
        
url = urljoin(url, form_details["action"])

if form_details["method"] == "post":
    res = session.post(url, data=data)
elif form_details["method"] == "get":
    res = session.get(url, params=data)
    

#example output
sampleLocation = "PROTECTION ENGINE CO #1 14 S WASHINGTON ST PT WASHINGTON, 11050\nhttps://www.google.com/maps/place/14%20S%20WASHINGTON%20ST,%20PT%20WASHINGTON,%2011050"
print("Your suggested polling location is: " + sampleLocation)
    


#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import getpass
import io
import sys
import re
import os.path

seshy = requests.Session()
page = seshy.get('https://intranet.hbtn.io/auth/sign_in', allow_redirects=True)
soup = BeautifulSoup(page.content, 'html.parser')

authtok = soup.find('input', attrs={'name':'authenticity_token'})
authtok = authtok['value']

print("-------------------------------------------------------")
print("Holberton officially unofficial project file scraper :)")
print("-------------------------------------------------------")
project_number = input("Project Number (Or full URL): ")
username = input("Enter your Intranet username: ") 
password = getpass.getpass()
print("-----")

print("Logging into user \'{}\'".format(username))

pload = {'authenticity_token':authtok, 'user[login]':username,'user[password]':password, 'commit':'Log in'}

seshy.post('https://intranet.hbtn.io/auth/sign_in', data = pload)

if ("http" in project_number):
    page = seshy.get(project_number, allow_redirects=False, data = pload)
else:
    page = seshy.get('https://intranet.hbtn.io/projects/' + project_number, allow_redirects=False, data = pload)



if (page.status_code is 200):
    print("Login Successful - Lets get to work...")
else:
    print("---")
    print("Login Failed with code {}".format(page.status_code))
    print("Check your username, password and your URL.")
    print("You could also be recieving this error because you do not have access to a project")
    sys.exit(1)

soup = BeautifulSoup(page.content, 'html.parser')

projects = soup.find_all("code")
""" Find all main/test files """
for i in projects:
    if "cat " in i.text:
        filename = str(i)
        filename = filename[(filename.find("cat ") + 4):len(filename)]
        if ("guil" in filename):
            code = filename[filename.find("\n"):filename.find("guil")]
        elif ("juli" in filename):
            code = filename[filename.find("\n"):filename.find("juli")] 

        filename = filename[0:filename.find("\n")]

        if (os.path.isfile(filename)):
            print("Ignored (File already exists): ", filename)
        else:
            f = open(filename, "w+")
            f.write(code)
            f.close()
            print("Created (test/main file):", filename) 


print("-----------------------------------------------")
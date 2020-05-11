#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import getpass
import io
import re
import os.path, sys, stat


if len(sys.argv) < 2 or "help " in sys.argv[1]:
    print("")
    print("USAGE: intranet (Project Number or Project URL)")
    print("Ex. intranet https://intranet.hbtn.io/projects/243")
    print("")
    sys.exit(1)

""" Create a session to retrieve the auth token 
    We need to use a session to persist the login info 
    throughout our scraping as we will need to navigate
    to the project page 
"""
seshy = requests.Session()
page = seshy.get('https://intranet.hbtn.io/auth/sign_in', allow_redirects=True)
soup = BeautifulSoup(page.content, 'html.parser')

authtok = soup.find('input', attrs={'name':'authenticity_token'})
authtok = authtok['value']

print("-------------------------------------------------------")
print("Holberton officially unofficial project file scraper :)")
print("-------------------------------------------------------")
project_number = sys.argv[1]

""" Get Login info from the user, use getpass module to not show users password """
username = input("Enter Holberton Email (Or just the number): ") 
password = getpass.getpass()
print("-----")


""" Stuff to see if the user input a full username/link or just the numbers """
if ("@" not in username):
    username = username + "@holbertonschool.com"
if ("http" not in project_number):
    project_number = ('https://intranet.hbtn.io/projects/' + project_number)

print("Logging into user \'{}\' to access project \'{}\'".format(username, project_number))


""" Using the authenticity token from the get earlier, login to the intranet with the users info """
pload = {'authenticity_token':authtok, 'user[login]':username,'user[password]':password, 'commit':'Log in'}
seshy.post('https://intranet.hbtn.io/auth/sign_in', data = pload)

page = seshy.get(project_number, allow_redirects=False, data = pload)


""" Stuff to make sure the login was successful """
if (page.status_code is 200):
    print("Login Successful - Lets get to work...")
else:
    print("---")
    print("Login Failed with code {}".format(page.status_code))
    print("Check your username, password and your project URL.")
    sys.exit(1)


""" Find all main/test files 

    Search method: All test files generally exist in the <code> html tag
    and they are displayed using the cat command ex "cat 0-main.py" you can
    find most of them using the "cat " as the beginning index and a newline
    as the end index, which should give you the filename.
    After the \n I get everything to the name juli or guil because of the 
    commandline.

    It also gives executable perms to anything thats a .py file or a .sh file

"""
soup = BeautifulSoup(page.content, 'html.parser')
main_scrape = soup.find_all("code")

for i in main_scrape:
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
            if (".py" in filename or ".sh" in filename):
                os.chmod(filename, stat.S_IRWXG)
            f.close()
            print("Created (test/main file):", filename) 


""" Find all the project file names """
project_scrape = soup.find_all("li")
for result in project_scrape:
    if ("File: " in result):
        file_name = str(result)
        file_name = file_name[file_name.find("<code>") + 6:file_name.find("</code>")]

        if (os.path.isfile(file_name)):
            print("Ignored (File already exists): ", file_name)
        else:
            f = open(file_name, "w+")
            if (".py" in file_name):
                f.write("#!/usr/bin/python3\n")
                os.chmod(file_name, stat.S_IRWXG)
            elif (".sh" in file_name):
                f.write("#!/bin/bash\n")
                os.chmod(file_name, stat.S_IRWXG)
            elif (".c" in file_name):
                f.write("#include<stdio.h>\n#include<holberton.h>\n")
            f.close()
            print("Created (Project File):", file_name) 

print("-----------------------------------------------")

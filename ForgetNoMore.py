from __future__ import print_function

## EDIT THESE ##
yourEmailForGmail = 'PUT_YOUR_GMAIL_HERE'
yourPasswordForGmail = 'PUT_YOUR_GMAIL_PASS_HERE'

## NO TOUCHY BELOW HERE ##
import httplib2
import os
import smtplib
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Happy Birthday Email'

def get_credentials():
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

    """
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1OxXAF2OlAP3HqEG0g4YbQUZ4X5pc0XNl_j1vpjDb6-g
    """
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

spreadsheetId = '1OxXAF2OlAP3HqEG0g4YbQUZ4X5pc0XNl_j1vpjDb6-g'
rangeName = 'Class Data!A2:E'
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetId, range=rangeName).execute()
values = result.get('values', [])


"""
# Binary search, currently disabled, however enable if you like
def binarySearch(lis, x):
    if len(lis) == 0:
        return False
    else:
        midpoint = len(lis)//2
        if lis[midpoint]==x:
            return True
        else:
            if x<lis[midpoint]:
                return binarySearch(lis[:midpoint],x)
            else:
                return binarySearch(lis[midpoint+1:],x)
"""

def emailText(filePath, name):
    return open(filePath).read().replace('xxx', name)

def sendMail(emailX, name):
    yourEmail = yourEmailForGmail
    password = yourPasswordForGmail

    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)

    server.login(yourEmail, password) 
    

    msg = emailText('email.txt', name)
    server.sendmail(yourEmail, emailX, msg)
    server.quit()

# yyyy/dd/mm in the end
current_time = str(datetime.datetime.now())
current_time = current_time.replace('-','/')
current_time = current_time[:10]
z = current_time.split('/')
z[1],z[2]=z[2],z[1]

z = '/'.join(z)
ct = z
print(ct)
# remove utf
# newLst = [x[1].encode('utf-8') for x in values]
if not values:
    print('No data found.')
else:
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        # print('%s, %s' % (row[0], row[1]))
        dob = str(row[1]).split('/')
        if (len(dob) > 2):
            dob[0],dob[2]=dob[2],dob[0]
            dob = '/'.join(dob)
            # print(ct + " " + dob)
            if (ct == dob):
                sendMail(row[2], row[0])

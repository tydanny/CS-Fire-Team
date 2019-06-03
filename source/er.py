import http
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import http.client
import datetime
from getpass import getpass
from dbconnect import dbconnect

def load_incidents(username=None, password=None, **kwargs):
    if username == None:
        username = input("Enter your username: ")
    
    db = dbconnect()
    
    access_token = get_token_pass(username, password)
    
    incidentIDs = get_incidents(access_token, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))

    c = []
    n = []
    
    for incident in incidentIDs: 
        n.append(incident['incidentNumber'])
        exposureID = get_exposureIDs(incident['incidentID'], access_token)

        crewMembers = get_crewMembers(exposureID[0]['exposureID'], access_token)
        
        #The 0 will be changed to a call once we figure out how to get the start time.
        db.load_incident(incident['incidentNumber'], incident['incidentDateTime'], exposureID['incidentType'], 0)
        
        #May need to chance the parameter, userID might not be the one we need.
        for member in crewMembers:
            db.load_person_xref_shift(incident['incidentNumber'], member['userID'])
            c.append(get_user(member['userID'], access_token)['fullName'])

    return n
    
    
def get_auth(username, password):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    }

    params = urllib.parse.urlencode({
    })

    body = { "response_type": "code", "client_id": "city_of_golden", "username": username, "password": password, "state": "xyz" }
    j = json.dumps(body)
    #body = '{ "response_type": "code", "client_id": "city_of_golden", "username": %s, "password": %s, "state": "xyz" }' % (username, password)

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("POST", "/auth/Authorize.php?%s" % params, j, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        return data[33:73]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_token_pass(username, password=None):

    if password == None:
        password = get_pass()

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    }

    params = urllib.parse.urlencode({
    })

    body = { 
        "grant_type": "password",
        "client_id": "city_of_golden",
        "client_secret": "d4f030ead6c2d25aed4a57ad8912f90c7f5668a0",
        "username": username,
        "password": password
    }
    j = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("POST", "/authpass/Token.php?%s" % params, j, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        return data["access_token"]
    except Exception as e:
        print(data)
        print(e)

def get_token(auth_code):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    }

    params = urllib.parse.urlencode({
    })

    body = {
      "grant_type": "authorization_code", 
      "code" : auth_code,
      "client_id": "city_of_golden", 
      "client_secret" : "d4f030ead6c2d25aed4a57ad8912f90c7f5668a0",
      "redirect_uri" : "https://google.com"
    }
    j = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("POST", "/authtoken/Token.php?%s" % params, j, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        return data['access_token']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_incidents(access_token, **kwargs):
    frmtstr = '%Y-%m-%d'

    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    if start_date == None:
        start = datetime.datetime.strptime(input("Enter start date (yyyy-mm-dd): "), frmtstr)
    elif type(start_date) == str:
        start = datetime.datetime.strptime(start_date, frmtstr)
    elif type(start_date) == datetime.datetime:
        start = start_date
    else:
        raise TypeError('Invalid start date type')

    if end_date == None:
        end = datetime.datetime.strptime(input("Enter end date (yyyy-mm-dd): "), frmtstr)
    elif type(end_date) == str:
        end = datetime.datetime.strptime(end_date, frmtstr)
    elif type(end_date) == datetime.datetime:
        end = end_date
    else:
        raise TypeError('Invalid end date type')

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        'filter': 'incidentDateTime ge "%s", incidentDateTime le "%s"' % (start.date().isoformat(), end.date().isoformat()),
        'orderby': 'incidentDateTime ASC'
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/incidents?%s" % params, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        return data['incidents']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_pass():
    try:
        return getpass(prompt="Enter your password: ")
    except Exception as e:
        print('Password Error: ', e)

def get_exposureIDs(incidentID, access_token):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/incidents/%s/exposures?%s" % (incidentID, params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['exposures']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_crewMembers(exposureID, access_token):
    headers = {
         # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/exposures/%s/crewmembers?%s" % (exposureID, params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['crewMembers']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_user(userID, access_token):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyusers/users/%s?%s" % (userID, params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['user']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


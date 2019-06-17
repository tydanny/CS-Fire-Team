import http
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import http.client
import datetime
from getpass import getpass
from source import dbconnect

"""
This module handles all interaction with the api and the database.
Any data pulled from Emergency Reporting is pulled through the
API using the functions below.
"""

def update(access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'),kwargs.get('password'))

    start, end = get_dates(kwargs.get('start_date'), kwargs.get('end_date'))

    load_people(access_token)
    load_incidents(access_token, start_date=start, end_date=end)
    load_events(access_token, start_date=start, end_date=end)
    load_trainings(access_token, start_date=start, end_date=end)

def load_incidents(access_token=None, **kwargs):
    try:
        if access_token == None:
            access_token = get_token_pass(kwargs.get('username'),kwargs.get('password'))
        
        db = dbconnect.dbconnect()

        start, end = get_dates(kwargs.get('start_date'), kwargs.get('end_date'))
        
        incidentsList = get_incidents(access_token, start_date=start, end_date=end)

        incidents = {}

        for incident in incidentsList:
            incidents[incident['incidentID']] = (incident['incidentDateTime'], [])

        xref = db.get_incident_people(start, end)
        for pair in xref:
            incidents[str(pair[1])][1].append(pair[0])

        exposures = get_exposures(access_token)
        crewMembers = get_crewMembers(access_token)
        users = get_uids(access_token)
        
        for exposure in exposures:
            if exposure['incidentID'] in incidents.keys():
                    db.load_incident(exposure['incidentID'], incidents[exposure['incidentID']][0], exposure['incidentType'], 0)
                    for member in crewMembers[exposure['exposureID']]:
                        if users[member] != 'None' and users[member] not in incidents[exposure['incidentID']][1]:
                            db.load_person_xref_incident(exposure['incidentID'], users[member])
    except Exception as e:
        f = open("incidents.log", "a")
        f.write(str(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6)))
        f.write("%s \n %s \n %s \n %s \n \n" % (e, exposure['incidentID'], exposure['exposureID'], member))
    
def get_auth(username, password):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080'
    }

    params = urllib.parse.urlencode({
    })

    body = { "response_type": "code", "client_id": "city_of_golden", "username": username, "password": password, "state": "xyz" }
    j = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("POST", "/auth/Authorize.php?%s" % params, j, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        return data[33:73]
    except Exception as e:
        raise(e)

def get_token_pass(username=None, password=None):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    }

    params = urllib.parse.urlencode({
    })

    while True:
        if username == None:
            username = input("Enter your username: ")

        if password == None:
            password = get_pass()

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
            if 'error' not in data.keys():
                return data["access_token"]
        except Exception as e:
            raise(e)

        print(data)
        password = None
        username = None

def get_token_ref(username=None, password=None):

    if username == None:
        username = input("Enter your username: ")

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
        return data
    except Exception as e:
        raise(e)

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
        conn.close()
        return data['access_token']
    except Exception as e:
        raise(e)

def get_incidents(access_token, **kwargs):

    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    start, end = get_dates(start_date, end_date)

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        'filter': 'incidentDateTime ge "%s", incidentDateTime le "%s"' % (start.date().isoformat(), end.date().isoformat()),
        'orderby': 'incidentDateTime ASC',
        'limit': 9999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/incidents?%s" % params, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        return data['incidents']
    except Exception as e:
        raise(e)

def get_dates(start_date, end_date):
    frmtstr = '%Y-%m-%d'

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
    return start, end

def get_pass():
    try:
        return getpass(prompt="Enter your password: ")
    except Exception as e:
        print('Password Error: ', e)

def get_exposures(access_token=None, **kwargs):
    
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'),kwargs.get('password'))

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 99999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/incidents/exposures?%s" % (params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['exposures']
    except Exception as e:
        raise(e)

def get_crewMembers(access_token=None, **kwargs):

    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'),kwargs.get('password'))

    headers = {
         # Request headers
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 99999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/exposures/crewmembers?%s" % (params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        crewDict = {}
        for crewMember in j['crewMembers']:
            if crewMember['exposureID'] not in crewDict.keys():
                crewDict[crewMember['exposureID']] = []
            crewDict[crewMember['exposureID']].append(crewMember['userID'])
        return crewDict
    except Exception as e:
        raise(e)

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
        if j:
            return j['user'] 
        else:
            return None
    except Exception as e:
        raise(e)

def get_my_user(access_token=None):

    if access_token == None:
        access_token = get_token_pass()

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyusers/users/me?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        j = json.loads(data)
        return j['user']
    except Exception as e:
        raise(e)

def get_events(access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'),kwargs.get('password'))

    start, end = get_dates(kwargs.get('start_date'), kwargs.get('end_date'))

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'dd47ea607c5648dc8c2677b5fe8c6126',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'filter': 'eventDateTime ge "%s", eventDateTime lt "%s"' % (start.date().isoformat(), end.date().isoformat()),
        'orderby': 'eventDateTime ASC',
        'limit': 999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyevents/events?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['events']
    except Exception as e:
        raise(e)

def load_events(access_token=None, **kwargs):
    try:
        if access_token == None:
            access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

        events = get_events(access_token, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
        eventCatList = get_event_cat(access_token)

        eventCats = {}
        
        db = dbconnect.dbconnect()

        for eventCat in eventCatList:
            eventCats[eventCat['eventCategoriesID']] = eventCat['category']
        
        eventIDs = []
        for event in events:
            db.load_event(event['eventsID'], event['eventEndDate'], eventCats[event['eventCategoryID']])
            eventIDs.append(event['eventsID'])

        load_events_xref(eventIDs, access_token)
    except Exception as e:
        f.write(str(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6)))
        f.write(e)
        print(e)
    

def load_events_xref(eventIDs, access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    db = dbconnect.dbconnect()
    attendees = get_event_people(access_token)
    users = get_uids(access_token)
    for attendee in attendees:
        if attendee['eventID'] in eventIDs:
            db.load_person_xref_event(attendee['eventID'], users[attendee['userID']], attendee['hours'])

def get_uids(access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'dd47ea607c5648dc8c2677b5fe8c6126',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 1000,
    })


    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyusers/users?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        j = json.loads(data)
        conn.close()
        users = {}

        for user in j['users']:
            users[str(user['userID'])] = str(user['agencyPersonnelID'])

        return users
    except Exception as e:
        raise(e)

def get_event_cat(access_token=None, **kwargs):
    
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))
        
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'dd47ea607c5648dc8c2677b5fe8c6126',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        "limit": 100
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyevents/events/categories?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        if j:
            return j['eventCategories']
        else:
            return None
    except Exception as e:
        raise(e)


def get_event_people(access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'dd47ea607c5648dc8c2677b5fe8c6126',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 1000000
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyevents/events/people?%s"% (params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j["eventPeople"]
    except Exception as e:
        raise(e)

def get_people(access_token=None, **kwargs):

    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 10000
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyusers/users?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['users']
    except Exception as e:
        raise(e)


def load_people(access_token=None, **kwargs):
    try:
        if access_token == None:
            access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

        users = get_people(access_token)
        db = dbconnect.dbconnect()
        
        ids = db.get_ids()
        idDict = {}
        for id in ids:
            idDict[id[0]] = (id[1], id[2], id[3], id[4])

        for u in users:
            if u['agencyPersonnelID'] not in idDict.keys() and u['agencyPersonnelID'] != None:
                l, f = u['fullName'].split(', ', 1)
                if "'" in l:
                    l = l.replace("'", r"''")
                if "'" in f:
                    f = f.replace("'", r"''")
                db.load_person(u['agencyPersonnelID'], f, l, u['title'], u['shift'])
            elif u['agencyPersonnelID'] != None:
                if u['shift'] != idDict[u['agencyPersonnelID']][0]:
                    db.update_residency(u['agencyPersonnelID'], u['shift'])
                l, f = u['fullName'].split(', ', 1)
                if l != idDict[u['agencyPersonnelID']][2]:
                    db.update_lname(u['agencyPersonnelID'], l)
                if f != idDict[u['agencyPersonnelID']][3]:
                    db.update_fname(u['agencyPersonnelID'], f)
                if u['title'] != idDict[u['agencyPersonnelID']][1]:
                    db.update_title(u['agencyPersonnelID'], u['title'])
    except Exception as e:
        f = open("people.log", "a")
        f.write(str(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6)))
        f.write(e)
        print(e)

def get_event_types(access_token=None, **kwargs):
    
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))
        
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'dd47ea607c5648dc8c2677b5fe8c6126',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyevents/events/types?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['eventTypes']
    except Exception as e:
        raise(e)

def refresh(refresh_token):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    }

    body = {
        "grant_type": "refresh_token", 
        "client_id": "city_of_golden", 
        "client_secret" : "d4f030ead6c2d25aed4a57ad8912f90c7f5668a0", 
        "refresh_token" : refresh_token
    }

    j = json.dumps(body)

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("POST", "/refreshtoken/Token.php?%s" % params, j, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        return data
    except Exception as e:
        raise(e)


def load_trainings_xref(classIDs, access_token=None, **kwargs):

    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    db = dbconnect.dbconnect()
    users = get_uids(access_token)
    students = get_students(access_token)
    
    for student in students:
        if student['classID'] in classIDs and student['studentUserID'] in users.keys():
            db.load_person_xref_class(student['classID'], users[student['studentUserID']], student['hours'])   


def get_students_class(classID, access_token=None, **kwargs):
    if access_token == None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '9fabb21336d64b24a7774cf528ea8e46',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 9999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyclasses/classes/%s/students?%s" % (classID, params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['students']
    except Exception as e:
        raise(e)

def get_trainings(access_token=None, **kwargs):

    if access_token==None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    start, end = get_dates(kwargs.get('start_date'), kwargs.get('end_date'))
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '9fabb21336d64b24a7774cf528ea8e46',
        'Authorization': access_token
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 999999,
        'filter': 'classDate ge %s, classDate le %s' % (start, end)
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyclasses/classes?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['classes']
    except Exception as e:
        raise(e)

def get_training_cat(access_token=None, **kwargs):

    if access_token==None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))
        
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '9fabb21336d64b24a7774cf528ea8e46',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyclasses/classes/categories?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['categories']
    except Exception as e:
        raise(e)

def get_students(access_token=None, **kwargs):

    if access_token==None:
        access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '9fabb21336d64b24a7774cf528ea8e46',
        'Authorization': access_token,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'limit': 9999999
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyclasses/classes/students?%s" % (params), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        j = json.loads(data)
        conn.close()
        return j['students']
    except Exception as e:
        raise(e)

def load_trainings(access_token=None, **kwargs):
    try:
        if access_token == None:
            access_token = get_token_pass(kwargs.get('username'), kwargs.get('password'))

        db = dbconnect.dbconnect()

        trainings = get_trainings(access_token, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
        trainingCatList = get_training_cat(access_token)

        trainingCats = {}
        
        for trainingCat in trainingCatList:
            trainingCats[trainingCat['categoryID']] = trainingCat['name']
        
        trainingIDs = []
        for training in trainings:
            db.load_class(training['classID'], training['classDate'], trainingCats[training['classCategoryID']])
            trainingIDs.append(training['classID'])
            print(training['classDate'])

        load_trainings_xref(trainingIDs, access_token)
    except Exception as e:
        f = open("trainings.log", "a")
        f.write(str(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6)))
        f.write(e)
        print(e)
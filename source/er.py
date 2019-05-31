import http
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import http.client

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

def get_incident(auth_token):
    
    headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '1e9590cf0a134d4c99c3527775b03080',
    'Authorization': auth_token,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('data.emergencyreporting.com')
        conn.request("GET", "/agencyincidents/incidents/9999999?%s" % params, headers=headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

      

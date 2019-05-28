import http
import urllib.request
import urllib.parse
import urllib.error
import base64
import json

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
        print(data[33:73])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
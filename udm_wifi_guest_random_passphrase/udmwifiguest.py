import requests
import json
import sys
import base64
import random
import itertools
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

###########
# SETTINGS
#

# UDM settings
UDM_USR = 'admin'
UDM_PWD = 'fooblasuperpasword'
GUEST_WLAN_ID = '123ad56f123ad56f123ad56f'
HOST = '192.168.1.1'
UDMWIFIGUESTPATH = '/mnt/data/udmwifiguest'
# random passphrase settings
nwords = 5
nbits = 12
filename = 'wordlist'

###########
"""
Do not modify anything below this line unless you know what you are doing
"""

def read_file(filename, nbits):
    return [line.split()[1] for line in
            itertools.islice(open(filename), 2**nbits)]

def generate_password(nwords, wordlist):
    choice = random.SystemRandom().choice
    return ' '.join(choice(wordlist) for ii in range(nwords))

# Fix incorrect padding for base64 string
def pad_base64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '='* (4 - missing_padding)
    return data

# Open session
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {"Accept": "application/json","Content-Type": "application/json"}
s = requests.Session()

# Authenticate
data = {'username': UDM_USR, 'password': UDM_PWD}
r = s.post('https://{}/api/auth/login'.format(HOST),
    headers = headers,  json=data, verify=False, timeout=1)
if r.status_code != 200:
    print("Authentication failed")
    sys.exit(1)

# Extract CSRF token from cookie
token = pad_base64(s.cookies['TOKEN'].split('.')[1])
data = json.loads(base64.b64decode(token))
csrf_token = data['csrfToken']

# Generate random passphrase
wordlist = read_file(os.path.join(UDMWIFIGUESTPATH, filename), nbits)
WIFI_PASSPHRASE = generate_password(nwords, wordlist)

# Update wifi passphrase
data = { "x_passphrase": WIFI_PASSPHRASE }
headers["x-csrf-token"] = csrf_token
r = s.put('https://{}/proxy/network/api/s/default/rest/wlanconf/{}'.format(HOST, GUEST_WLAN_ID),
    json=data, headers=headers, verify=False, timeout=1)
#print(r.text)

# Write wifi passphrase to wifi.txt
with open(os.path.join(UDMWIFIGUESTPATH, "wifi"), "w") as text_file:
    text_file.write(WIFI_PASSPHRASE)


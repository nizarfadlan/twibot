# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import time
import json
import math
import re
import requests

url = 'https://10minutemail.com'
r = requests.Session()

def runEmail():
  try:
    r.get(url)
    return True
  except:
    return False

def getEmail():
  try:
    page = r.get(f'{url}/session/address')
    email = page.json()
    return email['address']
  except:
    return False

def getCountSeconds():
  try:
    page = r.get(f'{url}/session/secondsLeft')
    count = page.json()
    minutes = math.floor(int(count['secondsLeft'])/60)
    seconds = int(count['secondsLeft'])-minutes*60
    time = f'{minutes}:{seconds} Minute'
    return time
  except:
    return False

def getCountBox():
  try:
    page = r.get(f'{url}/messages/messageCount')
    count = page.json()
    return count['messageCount']
  except:
    return False

def getCodeVerifTwitter():
  try:
    page = r.get(f'{url}/messages/')
    box = page.json()
    count = getCountBox()
    count = int(count)-1
    body = box[count]['bodyPlainText']
    code = re.findall(r'\d+', body)[0]
    return code
  except:
    return False

def longActive():
  try:
    r.get(f'{url}/session/reset')
    return True
  except:
    return False

def clearCookie():
  try:
    r.cookies.clear()
    return True
  except:
    return False

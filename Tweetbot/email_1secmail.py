# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import requests
import random
import string
import time
import re

domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
url = 'https://www.1secmail.com/api/v1/'
domain = random.choice(domainList)

def username():
  name = string.ascii_lowercase + string.digits
  username = ''.join(random.choice(name) for i in range(10))
  return username

newMail = f'{url}?login={username()}&domain={domain}'

def extract():
  getUserName = re.search(r'login=(.*)&', newMail).group(1)
  getDomain = re.search(r'domain=(.*)', newMail).group(1)
  return [getUserName, getDomain]

def runEmail():
  try:
    reqMail = requests.get(newMail)
    mail = f'{extract()[0]}@{extract()[1]}'
    return mail
  except:
    return False

def deleteMail():
  data = {
      'action': 'deleteMailbox',
      'login': f'{extract()[0]}',
      'domain': f'{extract()[1]}'
  }

  req = requests.post('https://www.1secmail.com/mailbox', data=data)

def checkMails():
  reqLink = f'{url}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
  req = requests.get(reqLink).json()
  length = len(req)
  return length

def getCodeVerifTwitter():
  reqLink = f'{url}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
  req = requests.get(reqLink).json()

  idList = []
  for i in req:
    for k,v in i.items():
      if k == 'id':
        mailId = v
        idList.append(mailId)

  for i in idList:
    msgRead = f'{url}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
    req = requests.get(msgRead).json()
    for k,v in req.items():
      if k == 'from':
        sender = v
      if k == 'subject':
        subject = v
      if k == 'date':
        date = v
      if k == 'textBody':
        content = v

    if sender.split('@')[1] == 'bounce.twitter.com':
      code = re.findall(r'\d+', content)[0]
      return code
    else:
      return False

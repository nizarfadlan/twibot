# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import sys
from .utils import Color

def Help(e):
  if e == 1:
    print(Color('cr'))
    print('')
    print('Usage: python main.py [-t] [-r {link tweet}] [-q {link tweet}] [-p {link tweet}]')
    print('')
    print('-t or --tweet: ')
    print('')
    print('        This is for the tweet menu')
    print('')
    print('-r or --retweet: ')
    print('')
    print('        This is for the retweet menu')
    print('')
    print('-q or --quote: ')
    print('')
    print('        This is for the quote retweet menu')
    print('')
    print('-p or --reply: ')
    print('')
    print('        This is for the reply tweet menu')
    print('')
    print('-h or --help: ')
    print('')
    print('        Help doc')
    print('')
    print('-i or --info: ')
    print('')
    print('        To see info')
    print('')
    print('-u or --usage: ')
    print('')
    print('        To see example usage bot')
    print('')
    print('For the account used, you can set it in the account.csv file')
    print('For tweet wordlist, you can set it in wordlist.csv')
    print('')
    print('Install the required libraries: ')
    print('    pip install -r requirements.txt')
    print('To see info: ')
    print('    python main.py -a or --about')
    print('Help: ')
    print('    python main.py -h or --help')
    print('How to change driver: ')
    print('    python main.py -d or --driver')
    print(Color('cend'))
  elif e == 2:
    print(Color('cr'))
    print('Error :')
    print('Make sure that your Chrome window are in Desktop mode.')
    print(Color('cend'))
  elif e == 3:
    print(Color('cr'))
    print('Error :')
    print('Execute "pip install -r requirements.txt" on command line.')
    print(Color('cend'))
  elif e == 4:
    print(Color('cy'))
    print('Warning :')
    print('Check if the internet connection is on.')
    print(Color('cend'))
  elif e == 5:
    print()
    print('twibot v1.0.1')
    print('This project is under MIT License.')
    print('To know about twibot: ')
    print('This project is kept on   https://github.com/nizarfadlan/twibot')
    print('Nizar')
    print('https://nizar.nfitec.com')
  elif e == 6:
    print(Color('cr'))
    print('')
    print('Change the chromedriver in the folder according to the version of chrome you have installed')
    print('Chromedriver download site :')
    print('https://chromedriver.chromium.org/downloads')
    print(Color('cend'))
  sys.exit()

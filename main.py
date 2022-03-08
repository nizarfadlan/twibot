# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import getopt, sys, datetime, socket, os, json
from Tweetbot import *

def show(description, version):
  logo = '''
          +                +++++++++* ++++
          +++++           +++++++++++++++++:
          +++++++++      ++++++++++++++++++#
          *++++++++++++++++++++++++++++++
          ++++++++++++++++++++++++++++++
          ++++++++++++++++++++++++++++++
            +++++++++++++++++++++++++++
            +++++++++++++++++++++++++
              +++++++++++++++++++++++
        +++++++++++++++++++++++++*
        +++++++++++++++++++++++
            +++++++++++++++
                                                  '''
  print(Color('cbl'),logo,Color('cend'))
  print(Color('cg'))
  print('\t',description)
  print('\t Version',version)
  print(Color('cend'))

def write_log(e):
  f = open('twibot_log.txt', 'a+')
  f.write(f'----------- {str(datetime.datetime.now())} ----------\n')
  f.write(str(e) + '\r\n')
  f.close()

def check_connection(host='8.8.8.8', port=53) -> None:
  try:
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except Exception as e:
    write_log(e)
    return False

def clear() -> None:
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')

# ------- MAIN -------

def main(argv):
  with open('config.json') as json_data:
    cfg = json.load(json_data)

  # ------- READ INPUT FROM CLI -------
  show('Twibot by Nizar', 'v1.0.1')
  print()

  # ------- CHECK CONNECTION -------

  network_status = check_connection()
  if not network_status:
    Help(4)

  try:
    options, remainder = getopt.getopt(
      argv,
      'ihautr:q:p:c:l:',
      ['install','help','about','usage','tweet','retweet=','quote=','reply=','create=','like='],
    )
  except getopt.GetoptError:
    print(f'{Color("cr")}There is a mistake!!{Color("cend")}')
    print('python main.py -h')
    sys.exit(2)

  for opt, arg in options:
    if opt in ('-i', '--install'):
      Help(6)
    elif opt in ('-h', '--help'):
      Help(1)
    elif opt in ('-a', '--about'):
      Help(5)
    elif opt in ('-u', '--usage'):
      Help(1)
    elif opt in ('-t', '--tweet'):
      clear()
      tweet(1, arg, cfg['AiTextGeneration']['status'], cfg['tweet']['hashtag'], cfg['tweet']['tag'])
    elif opt in ('-r', '--retweet'):
      clear()
      tweet(2, arg)
    elif opt in ('-q', '--quote'):
      clear()
      tweet(3, arg, cfg['AiTextGeneration']['status'], cfg['tweet']['hashtag'], cfg['tweet']['tag'])
    elif opt in ('-p', '--reply'):
      clear()
      tweet(4, arg, cfg['AiTextGeneration']['status'], cfg['tweet']['hashtag'], cfg['tweet']['tag'])
    elif opt in ('-l', '--like'):
      clear()
      tweet(5, arg)
    elif opt in ('-c', '--create'):
      if cfg['create']['password'] == '':
        print(f'{Color("cr")}First setting in the config password used in the account will be created later{Color("cend")}')
      else:
        if cfg['create']['typeProvider'] == 1:
          clear()
          minutemail(arg, cfg['create']['password'])
        elif cfg['create']['typeProvider'] == 2:
          clear()
          secmail(arg, cfg['create']['password'])
        else:
          print(f'{Color("cr")}First setting in the email provider config used!!!{Color("cend")}')
          sys.exit(2)

if __name__ == '__main__':
  main(sys.argv[1:])

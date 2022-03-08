# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

def Color(c):
  if c == 'cend':
    return '\033[0m'
  elif c == 'cb':
    return '\033[30m'
  elif c == 'cw':
    return '\033[37m'
  elif c == 'cr':
    return '\033[31m'
  elif c == 'cbl':
    return '\033[34m'
  elif c == 'cg':
    return '\033[32m'
  elif c == 'cy':
    return '\033[33m'

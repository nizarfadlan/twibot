# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.1
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import csv
import socket
import time
import os
import random
import datetime
import getopt
import sys
import names
from .usage import Help
from .utils import Color
from .email_10minutemail import runEmail, getEmail, getCountSeconds, getCountBox, getCodeVerifTwitter, clearCookie

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

try:
  from selenium import webdriver
  from selenium.common.exceptions import NoSuchElementException
  from selenium.webdriver.common.action_chains import ActionChains
  from selenium.webdriver.chrome.options import Options
  from selenium.webdriver.support.ui import Select
except Exception as e:
  write_log(e)
  Help(3)

# ------- SECTION SET DRIVER -------

options = Options()
options.headless = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')

class Create:
  def __init__(self, name, email, password):
    self.driver = webdriver.Chrome(options=options)
    self.name = name
    self.email = email
    self.password = password

  def check_element(self,xpath):
    try:
      self.driver.find_element_by_xpath(xpath)
      return True
    except NoSuchElementException:
      return False

  def click_object(self,xpath):
    wait = 2
    driver = self.driver
    try:
      time.sleep(wait)
      fieldObject = driver.find_element_by_xpath(xpath)
      fieldObject.click()
    except NoSuchElementException:
      time.sleep(wait)
      fieldObject = driver.find_element_by_xpath(xpath)
      action = ActionChains(driver)
      action.move_to_element(fieldObject)
      action.click(fieldObject)
      action.perform()

  def createUser(self):
    check_element = self.check_element
    click_object = self.click_object
    name = self.name
    email = self.email
    password = self.password
    driver = self.driver
    driver.get('https://twitter.com/signup')
    time.sleep(4)

    click_object('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[5]')
    click_object('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[4]')

    try:
      input_name = driver.find_element_by_name('name')
      input_email = driver.find_element_by_name('email')
    except NoSuchElementException:
      time.sleep(3)
      input_name = driver.find_element_by_name('name')
      input_email = driver.find_element_by_name('email')

    input_name.clear()
    input_email.clear()
    input_name.send_keys(name)
    input_email.send_keys(email)

    time.sleep(2)

    try:
      Select(driver.find_element_by_id('SELECTOR_1')).select_by_value(str(random.randint(1,12)))
      time.sleep(1)
      Select(driver.find_element_by_id('SELECTOR_2')).select_by_value(str(random.randint(1,27)))
      time.sleep(1)
      Select(driver.find_element_by_id('SELECTOR_3')).select_by_value(str(random.randint(1980,2000)))
    except NoSuchElementException:
      time.sleep(3)
      Select(driver.find_element_by_id('SELECTOR_1')).select_by_value(str(random.randint(1,12)))
      time.sleep(1)
      Select(driver.find_element_by_id('SELECTOR_2')).select_by_value(str(random.randint(1,27)))
      time.sleep(1)
      Select(driver.find_element_by_id('SELECTOR_3')).select_by_value(str(random.randint(1980,2000)))

    time.sleep(3)

    check_complete = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[2]/div/div').get_attribute('aria-disabled')

    if check_complete != 'true':
      click_object('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[2]/div/div')

      time.sleep(2)

      click_object('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div/div[6]')

      time.sleep(2)

      check_notnow = check_element('//div[@class="css-1dbjc4n r-1awozwy r-14lw9ot r-1867qdf r-1jgb5lz r-pm9dpa r-1ye8kvj r-1rnoaur r-d9fdf6 r-mfjstv r-13qz1uu"]')

      if not check_notnow:
        check_verification = check_element('//input[@name="verfication_code"]')

        if check_verification:

          def verif_email():
            input_verification = driver.find_element_by_xpath('//input[@name="verfication_code"]')
            verif = False
            while not verif:
              time.sleep(5)
              check_box = getCountBox()
              print(f'Check Email Box {check_box}', end='\r', flush=True)

              if check_box <= 0:
                check_box = getCountBox()
                verif = False
              else:
                break

            code = getCodeVerifTwitter()
            input_verification.send_keys(code)
            time.sleep(2)
            click_object('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[2]/div/div')

          verif_email()
          time.sleep(4)

          check_phone = check_element('//input[@name="phone_number"]')

          if check_phone:
            print()
            time.sleep(3)

            value_region = Select(driver.find_element_by_xpath('//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-1fmj7o5 r-1loqt21 r-1qd0xha r-1inkyih r-rjixqe r-crgep1 r-1wzrnnt r-1ny4l3l r-t60dpp r-xd6kpl r-1pn2ns4 r-ttdzmv"]'))
            for region in value_region.options:
              value = region.get_attribute('value')
              text = region.get_attribute('innerText')
              print(f'{value} = {text}')

            print()
            print('Select an existing region, select it by typing the letter on the left')
            region_code = input('Enter code region: ')
            region_code = region_code.upper()
            try:
              Select(driver.find_element_by_xpath('//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-1fmj7o5 r-1loqt21 r-1qd0xha r-1inkyih r-rjixqe r-crgep1 r-1wzrnnt r-1ny4l3l r-t60dpp r-xd6kpl r-1pn2ns4 r-ttdzmv"]')).select_by_value(region_code)
            except NoSuchElementException:
              time.sleep(3)
              Select(driver.find_element_by_xpath('//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-1fmj7o5 r-1loqt21 r-1qd0xha r-1inkyih r-rjixqe r-crgep1 r-1wzrnnt r-1ny4l3l r-t60dpp r-xd6kpl r-1pn2ns4 r-ttdzmv"]')).select_by_value(region_code)

            time.sleep(2)

            input_phone = driver.find_element_by_xpath('//input[@name="phone_number"]')
            number = input('Enter the phone number: ')

            input_phone.send_keys(number)
            time.sleep(5)
            click_object('//div[@class="css-18t94o4 css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1fneopy r-o7ynqc r-6416eg r-lrvibr" and @role="button"]')

            time.sleep(3)

            click_object('//div[@data-testid="confirmationSheetConfirm"]')

            time.sleep(3)

            check_verification = check_element('//input[@name="verfication_code"]')

            if check_verification:

              def verif_code():
                skip = False
                while not skip:
                  input_verification = driver.find_element_by_xpath('//input[@name="verfication_code"]')
                  print(f'{Color("cr")}You can enter the number 1 to resend the code{Color("cend")}\n')
                  code = input('Enter the verfication code: ')

                  time.sleep(2)
                  if code == '1':
                    click_object('//span[@class="css-18t94o4 css-901oao css-16my406 r-1n1174f r-poiln3 r-bcqeeo r-qvutc0" and @role="button"]')

                    time.sleep(2)

                    click_object('//div[@class="css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-ymttw5 r-1yzf0co r-o7ynqc r-6416eg r-13qz1uu" and @role="menuitem"]')

                    skip = False
                  else:
                    input_verification.send_keys(code)
                    time.sleep(2)
                    click_object('//div[@class="css-18t94o4 css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1fneopy r-o7ynqc r-6416eg r-lrvibr" and @role="button"]')
                    break

              time.sleep(3)
              verif_code()
              time.sleep(3)

          # None Verif Number Phone
          try:
            input_password = driver.find_element_by_name('password')
          except NoSuchElementException:
            time.sleep(3)
            input_password = driver.find_element_by_name('password')

          input_password.send_keys(password)

          time.sleep(2)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div')

          time.sleep(3)

          click_object('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]')

          time.sleep(3)
          if driver.current_url != 'https://twitter.com/home':
            time.sleep(10)
            print(f'{Color("cr")}Looks like registration is not perfect{Color("cend")}')
        else:
          print(f'{Color("cr")}Skip because the verification input does not appear{Color("cend")}')
      else:
        time.sleep(2)

        click_object('//div[@data-testid="confirmationSheetConfirm"]')

        print(f'{Color("cr")}Skip because Twitter was unable to complete your registration right now.{Color("cend")}')
    else:
      print(f'{Color("cr")}Skip because it doesn\'t fill in the input perfectly{Color("cend")}')

    driver.quit()

def minutemail(a,password):
  # ------- READ INPUT FROM CLI -------
  show('Twibot Create Account Email 10minutemail by Nizar', 'v1.0.1')
  print()
  print(f'Process started {datetime.datetime.now()}')
  i = 1
  while i <= int(a):
    try:
      runEmail()
      email = getEmail()
      if email:
        name = names.get_full_name()
        create = Create(name,email,password)
        print(f'Processing {str(i)}', end='\r', flush=True)
        print(f'Email {email} Remaining active email {getCountSeconds()}')
        create.createUser()
        f = open('./account_create.csv', 'a')
        w = csv.writer(f)
        w.writerow((email,password))
        clearCookie()
      else:
        print(f'Process failed connection on web email {str(email)}')
    except:
      print(f'Process failed {str(i)}')
      clearCookie()
    i += 1
  print(f'{Color("cg")}Process ended...{Color("cend")}')

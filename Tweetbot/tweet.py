# ///////////////////////////////////////////////////////////////
#
# CREATED: NIZAR IZZUDDIN Y.F
# V: 1.0.0
# GITHUB: https://github.com/nizariyf
#
# This project is free for everyone, if there is an error please contribute in this
#
# ///////////////////////////////////////////////////////////////

import time
import csv
import datetime
import socket
import getopt
import sys
import os
import random
import json
from .usage import Help
from .utils import Color

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
  from selenium import common
  from selenium.webdriver.common import keys
  from selenium.common.exceptions import NoSuchElementException
  from selenium.webdriver.chrome.options import Options
  from selenium.webdriver.common.action_chains import ActionChains
except Exception as ex:
  write_log(ex)
  Help(3)

# ------- SECTION DRIVER -------

options = Options()
options.headless = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

with open('./config.json') as json_data:
  cfg = json.load(json_data)

# ------- SECTION GPT NEO -------
def generate_word(word):
  from transformers import pipeline
  generator = pipeline('text-generation', model=cfg['AiTextGeneration']['model'])
  text = generator(word, max_length=50, do_sample=True, temperature=0.9)
  return text[0]['generated_text']

# ------- SECTION TWITTER BOT -------

class Twitter:

  def __init__(self, email, password):
    self.email = email
    self.password = password
    self.driver = webdriver.Chrome('./chromedriver.exe', options=options, service_log_path='NULL' if os.name == 'nt' else '/dev/null')
    self.bot = False
    self.skip = False
    self.is_logged_in = False

  def close_driver(self):
    self.driver.quit()

  def check_element(self,xpath):
    try:
      self.driver.find_element_by_xpath(xpath)
      return True
    except NoSuchElementException:
      return False

  def login(self):
    driver = self.driver
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(4)

    try:
      email = driver.find_element_by_name('text')
    except NoSuchElementException:
      time.sleep(3)
      email = driver.find_element_by_name('text')

    email.clear()
    email.send_keys(self.email)

    try:
      button_next = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[6]')
      ActionChains(driver).move_to_element(button_next).click(button_next).perform()
    except:
      time.sleep(2)
      email.send_keys(keys.Keys.RETURN)

    try:
      password = driver.find_element_by_name('password')
    except NoSuchElementException:
      time.sleep(3)
      password = driver.find_element_by_name('password')

    password.clear()
    password.send_keys(self.password)

    try:
      button_login = driver.find_element_by_xpath('//div[@data-testid="LoginForm_Login_Button"]')
      ActionChains(driver).move_to_element(button_login).click(button_login).perform()
    except:
      time.sleep(2)
      password.send_keys(keys.Keys.RETURN)

    time.sleep(7)

    if self.check_element('//form[@id="login-challenge-form"]') == True:
      print(f'{Color("cr")}    [x] Skip account due to code{Color("cend")}')
      write_log(f'Skip account {self.email} due to code')
      self.skip = True

    if self.check_element('//input[@type="tel"]') == True:
      print(f'{Color("cr")}    [x] Skip account due to code{Color("cend")}')
      write_log(f'Skip account {self.email} due to code')
      self.skip = True

    if driver.current_url == 'https://twitter.com/login/check':
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
      write_log(f'BOT account {self.email} detected')
      self.bot = True

    if driver.current_url == 'https://twitter.com/account/access':
      print(f'{Color("cr")}    [x] Account lock{Color("cend")}')
      write_log(f'Account {self.email} lock')
      self.skip = True

    if driver.current_url == 'https://twitter.com/login?username_disabled=true&redirect_after_login=%2F':
      print(f'{Color("cr")}    [x] Account disabled{Color("cend")}')
      write_log(f'Account {self.email} disabled')
      self.skip = True

    phone = ''

    if '+' in self.email:
      phone = self.email.split('+')
      phone = phone[1]

    if driver.current_url in [f'https://twitter.com/login/error?username_or_email=%2B{phone}&redirect_after_login=%2Fhome',f'https://twitter.com/login/error?username_or_email=%2B{phone}&redirect_after_login=%2F',f'https://twitter.com/login/error?username_or_email=%2B{self.email}&redirect_after_login=%2Fhome',f'https://twitter.com/login/error?username_or_email=%2B{self.email}&redirect_after_login=%2F']:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
      write_log(f'Skip account {self.email} because there is an error')
      self.skip = True

    if driver.current_url != 'https://twitter.com/home':
      time.sleep(10)

    self.is_logged_in = True

  def logout(self):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver
      driver.get('https://twitter.com/logout')
      time.sleep(3)

      while True:
        confirmButton = self.check_element('//div[@data-testid="confirmationSheetConfirm"]')
        if confirmButton:
          break
        time.sleep(3)
        continue

      try:
        driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]').click()
      except NoSuchElementException:
        time.sleep(3)
        confirmButton = driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]')
        ActionChains(driver).move_to_element(confirmButton).click(confirmButton).perform()

      time.sleep(3)
      self.is_logged_in = False
      driver.quit()

  def post_tweets(self,tweetBody):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver

      driver.get('https://twitter.com/compose/tweet')

      time.sleep(4)
      body = tweetBody
      print(f'    Tweet Word: {body}')

      while True:
        inputTweet = self.check_element('//div[@data-testid="tweetTextarea_0"]')
        if inputTweet:
          break
        time.sleep(3)
        continue

      try:
        driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
      except NoSuchElementException:
        time.sleep(3)
        driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)

      while True:
        max_word = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]').get_attribute('aria-valuenow')

        if int(max_word) != 100:
          time.sleep(4)

          try:
            driver.find_element_by_xpath('//div[@data-testid="tweetButton"]').click()
          except NoSuchElementException:
            time.sleep(2)
            tweetButton = driver.find_element_by_xpath('//div[@data-testid="tweetButton"]')
            ActionChains(driver).move_to_element(tweetButton).click(tweetButton).perform()

          print(f'{Color("cg")}    [+] Writing Successful Tweets{Color("cend")}')
          time.sleep(5)
          break
        else:
          len_delete_string = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]').text

          delete_string = len_delete_string if len_delete_string > 0 else 1

          body = body[:-int(delete_string):]
          try:
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
          except NoSuchElementException:
            time.sleep(3)
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
          continue


  # ------- RETWEET TWEET -------

  def retweet_tweet(self, tweetLink):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver

      time.sleep(4)
      tweetId = tweetLink.split('/status/')[1]
      driver.get(f'https://twitter.com/intent/retweet?tweet_id={tweetId}')
      time.sleep(4)

      if self.check_element('//article[@data-testid="tweet"]') == True:
        try:
          while True:
            confirmButton = self.check_element('//div[@data-testid="confirmationSheetConfirm"]')
            if confirmButton:
              break
            time.sleep(3)
            continue

          try:
            driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]').click()
          except NoSuchElementException:
            time.sleep(3)
            confirmButton = driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]')
            ActionChains(driver).move_to_element(confirmButton).click(confirmButton).perform()

          if self.check_element('//article[@data-testid="tweet"]//div[@data-testid="unlike"]') == False:
            try:
              driver.find_element_by_xpath('//article[@data-testid="tweet"]//div[@data-testid="like"]').click()
            except NoSuchElementException:
              time.sleep(2)
              button_like = driver.find_element_by_xpath('//article[@data-testid="tweet"]//div[@data-testid="like"]')
              ActionChains(driver).move_to_element(button_like).click(button_like).perform()

          print(f'{Color("cg")}    [+] Successfully retweet tweets{Color("cend")}')
          time.sleep(3)
        except:
          print(f'{Color("cr")}    [-] An error occurred{Color("cend")}')
      else:
        print(f'{Color("cr")}    [-] Tweet link doesn\'t exist{Color("cend")}')

  # ------- QUOTE RETWEET TWEET -------

  def quote_tweet(self, tweetLink, tweetWord):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver

      time.sleep(4)
      driver.get('https://twitter.com/compose/tweet')
      body = f'{tweetWord}\n{tweetLink}'
      time.sleep(4)

      if self.check_element('//div[@data-testid="tweetTextarea_0"]') == True:
        try:
          try:
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
          except NoSuchElementException:
            time.sleep(3)
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)

          while True:
            max_word = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]').get_attribute('aria-valuenow')

            if int(max_word) != 100:
              time.sleep(4)

              try:
                driver.find_element_by_xpath('//div[@data-testid="tweetButton"]').click()
              except NoSuchElementException:
                time.sleep(2)
                tweetButton = driver.find_element_by_xpath('//div[@data-testid="tweetButton"]')
                ActionChains(driver).move_to_element(tweetButton).click(tweetButton).perform()

              print(f'{Color("cg")}    [+] Writing Successful Tweets{Color("cend")}')
              time.sleep(4)
              break
            else:
              len_delete_string = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]').text

              delete_string = len_delete_string if len_delete_string > 0 else 1

              tweetWord = tweetWord[:-int(delete_string):]
              body = f'{tweetWord}\n{tweetLink}'
              try:
                driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
              except NoSuchElementException:
                time.sleep(3)
                driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(body)
              continue

          print(f'{Color("cg")}    [+] Successfully quote retweet tweets{Color("cend")}')
        except Exception as e:
          print(f'{Color("cr")}    [-] An error occurred{Color("cend")}')
          print(e)
      else:
        print(f'{Color("cr")}    [-] Tweet link doesn\'t exist{Color("cend")}')

  # ------- REPLY TWEET -------

  def reply_tweet(self, tweetLink, tweetWord):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver

      time.sleep(4)
      tweetId = tweetLink.split('/status/')[1]
      driver.get(f'https://twitter.com/intent/tweet?in_reply_to={tweetId}')
      time.sleep(4)

      if self.check_element('//article[@data-testid="tweet"]') == True:
        try:
          try:
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(tweetWord)
          except NoSuchElementException:
            time.sleep(3)
            driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(tweetWord)

          while True:
            max_word = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]').get_attribute('aria-valuenow')

            if int(max_word) != 100:
              time.sleep(4)

              try:
                driver.find_element_by_xpath('//div[@data-testid="tweetButton"]').click()
              except NoSuchElementException:
                time.sleep(2)
                tweetButton = driver.find_element_by_xpath('//div[@data-testid="tweetButton"]')
                ActionChains(driver).move_to_element(tweetButton).click(tweetButton).perform()

              print(f'{Color("cg")}    [+] Writing Successful Tweets{Color("cend")}')
              time.sleep(4)
              break
            else:
              len_delete_string = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div[3]/div').text

              delete_string = len_delete_string if len_delete_string > 0 else 1

              tweetWord = tweetWord[:-int(delete_string):]
              try:
                driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(tweetWord)
              except NoSuchElementException:
                time.sleep(3)
                driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(tweetWord)
              continue

          time.sleep(2)

          print(f'{Color("cg")}    [+] Successfully reply tweets{Color("cend")}')
        except Exception as e:
          print(f'{Color("cr")}    [-] An error occurred{Color("cend")}')
          print(e)
      else:
        print(f'{Color("cr")}    [-] Tweet link doesn\'t exist{Color("cend")}')

  # ------- LIKE TWEET -------

  def like_tweet(self, tweetLink):
    if self.is_logged_in == False:
      print(f'{Color("cr")}    [x] You must log in first!{Color("cend")}')
    elif self.skip == True:
      print(f'{Color("cr")}    [x] Skip account because there is an error{Color("cend")}')
    elif self.bot == True:
      print(f'{Color("cr")}    [x] BOT account detected{Color("cend")}')
    else:
      driver = self.driver

      time.sleep(4)
      tweetId = tweetLink.split('/status/')[1]
      driver.get(f'https://twitter.com/intent/like?tweet_id={tweetId}')
      time.sleep(4)

      if self.check_element('//article[@data-testid="tweet"]') == True:
        try:
          while True:
            confirmButton = check_element('//div[@data-testid="confirmationSheetConfirm"]')
            if confirmButton:
              break
            time.sleep(3)
            continue

          try:
            driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]').click()
          except NoSuchElementException:
            time.sleep(3)
            confirmButton = driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]')
            ActionChains(driver).move_to_element(confirmButton).click(confirmButton).perform()

          print(f'{Color("cg")}    [+] Successfully like tweets{Color("cend")}')
        except:
          print(f'{Color("cr")}    [-] An error occurred{Color("cend")}')
      else:
        print(f'{Color("cr")}    [-] Tweet link doesn\'t exist{Color("cend")}')

# ------- MENU -------
def tweet(a,link='',ai='',hashtag='',tag=''):
  # ------- READ INPUT FROM CLI -------
  show('Twibot by Nizar', 'v1.0.1')
  print()

  if hashtag == False:
    hashtag = ''
  if tag == False:
    tag = ''

  if a == 1:
    time_now = str(datetime.datetime.now())[:-7]
    print(f'TwitterBot started at {time_now} !')
    try:
      with open('./wordlist.csv','r') as word_obj:
        csv_word = csv.reader(word_obj)
        words_data = [d for d in csv_word]
        count_line = len(words_data)

      with open('./account.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
          for number, item in enumerate(csv_reader):
            number = number+1
            print(f'[*] Login account twitter {number}')
            print(f'    Username/Phone Number : {item[0]}')
            start = Twitter(item[0], item[1])
            start.login()

            #------- WORD RANDOM ------
            random_line = random.randint(0, count_line-1)
            count_words = len(words_data[random_line])
            random_word = random.randint(0, count_words-1)
            words = words_data[random_line][random_word]
            if ai == True:
              words = generate_word(words)
            word = f'{words}\n{tag}\n\n{hashtag}'

            start.post_tweets(word)
            start.logout()
            print(f'[*] Logout account twitter {number}')
    except Exception as e:
      start.close_driver()
      print(e)
      write_log(e)
  elif a == 2:
    time_now = str(datetime.datetime.now())[:-7]
    print(f'TwitterBot started at {time_now} !')
    link_tweet = link
    try:
      with open('./account.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
          for number, item in enumerate(csv_reader):
            number = number+1
            print(f'[*] Login account twitter {number}')
            print(f'    Username/Phone Number : {item[0]}')
            start = Twitter(item[0], item[1])
            start.login()
            start.retweet_tweet(link_tweet)
            start.logout()
            print(f'[*] Logout account twitter {number}')
    except Exception as e:
      start.close_driver()
      print(e)
      write_log(e)
  elif a == 3:
    time_now = str(datetime.datetime.now())[:-7]
    print(f'TwitterBot started at {time_now} !')
    link_tweet = link
    try:
      with open('./wordlist.csv','r') as word_obj:
        csv_word = csv.reader(word_obj)
        words_data = [d for d in csv_word]
        count_line = len(words_data)

      with open('./account.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
          for number, item in enumerate(csv_reader):
            number = number+1
            print(f'[*] Login account twitter {number}')
            print(f'    Username/Phone Number : {item[0]}')
            start = Twitter(item[0], item[1])
            start.login()

            #------- WORD RANDOM ------
            random_line = random.randint(0, count_line-1)
            count_words = len(words_data[random_line])
            random_word = random.randint(0, count_words-1)
            words = words_data[random_line][random_word]
            if ai == True:
              words = generate_word(words)
            word = f'{words}\n{tag}\n\n{hashtag}'

            start.quote_tweet(link_tweet, word)
            start.logout()
            print(f'[*] Logout account twitter {number}')
    except Exception as e:
      start.close_driver()
      print(e)
      write_log(e)
  elif a == 4:
    time_now = str(datetime.datetime.now())[:-7]
    print(f'TwitterBot started at {time_now} !')
    link_tweet = link
    try:
      with open('./wordlist.csv','r') as word_obj:
        csv_word = csv.reader(word_obj)
        words_data = [d for d in csv_word]
        count_line = len(words_data)

      with open('./account.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
          for number, item in enumerate(csv_reader):
            number = number+1
            print(f'[*] Login account twitter {number}')
            print(f'    Username/Phone Number : {item[0]}')
            start = Twitter(item[0], item[1])
            start.login()

            #------- WORD RANDOM ------
            random_line = random.randint(0, count_line-1)
            count_words = len(words_data[random_line])
            random_word = random.randint(0, count_words-1)
            words = words_data[random_line][random_word]
            if ai == True:
              words = generate_word(words)
            word = f'{words}\n{tag}\n\n{hashtag}'

            start.reply_tweet(link_tweet, word)
            start.logout()
            print(f'[*] Logout account twitter {number}')
    except Exception as e:
      start.close_driver()
      print(e)
      write_log(e)
  elif a == 5:
    time_now = str(datetime.datetime.now())[:-7]
    print(f'TwitterBot started at {time_now} !')
    link_tweet = link
    try:
      with open('./account.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
          for number, item in enumerate(csv_reader):
            number = number+1
            print(f'[*] Login account twitter {number}')
            print(f'    Username/Phone Number : {item[0]}')
            start = Twitter(item[0], item[1])
            start.login()
            start.like_tweet(link_tweet)
            start.logout()
            print(f'[*] Logout account twitter {number}')
    except Exception as e:
      start.close_driver()
      print(e)
      write_log(e)

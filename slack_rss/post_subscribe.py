import requests
import json
import sys
from pprint import pprint 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from subprocess import check_output



feeds_file = './slack_rss/feeds.txt'



# input(check_output(["pwd"]))

url = "https://safeescapetesting.slack.com/"
usernameId = "signup_email"
username = "adam.grandt@gmail.com"
submit_buttonId = "submit_btn"

rss_app_url = "https://safeescapetesting.slack.com/services/B06641DQBDL"
rss_chanel = "#api-testing"
rss_chanel_id = "C066MPZ84JD"
add_rss_submit_btn_id = "add_integration"

driver = webdriver.Chrome()

def login(url,usernameId, username, submit_buttonId):
   driver.get(url)
   try: 
      driver.find_element(By.ID, usernameId).send_keys(username)
      driver.find_element(By.ID, submit_buttonId).click()
   except NoSuchElementException:
      sys.exit(f'Could not find field Ids {usernameId} or {submit_buttonId}')



def add_feed(driver, rss_chanel_id, feed_url, add_rss_submit_btn_id):
   try: 
      feed_url_elem = driver.find_element(By.ID, "feed_url")
      feed_url_elem.clear()
      feed_url_elem.send_keys(feed_url)
   except NoSuchElementException:
      sys.exit(f'Could not find field Id feed_url')

   try: 
      # rss_chanel_elem = driver.find_element(By.ID, "feed_channel")
      # rss_chanel_elem.set_attribute("value", rss_chanel_id)
      driver.execute_script(f"$('#feed_channel').val('{rss_chanel_id}'); $('#feed_channel').change();")

      # $('#feed_channel').val('C066MPZ84JD'); $('#feed_channel').change();

   except NoSuchElementException:
      sys.exit(f'Could not find field id feed_channel')


   input('Befoire we submit how dose it look?')


   try: 
      driver.find_element(By.ID, add_rss_submit_btn_id).click()
   except NoSuchElementException:
      sys.exit(f'Could not find field id {add_rss_submit_btn_id}')



   
   input('how dose it look after?')

   

# Login to Slack
url  = input(f'What is the slack workspace URL, press enter for:  {url}') or url 
username  = input(f'What is the slack username, press enter for:  {username}') or username 
feeds_file  = input(f'What is the location of the feeds file, press enter for:  {feeds_file}') or feeds_file 

login(url, usernameId, username, submit_buttonId)
input('Please finish logging into slack and then click any button')

#Valdiate channel data 
rss_app_url  = input(f'What is the RSS app URL, press enter for:  {rss_app_url}') or rss_app_url 
rss_chanel_id = input(f'What is the RSS app URL, press enter for {rss_chanel} : {rss_chanel_id}') or rss_chanel_id

driver.get(rss_app_url)

input('Ready to add some feeds?: press enter to continue.')

#add some Feeds 
total = int(check_output(["wc", "-l", feeds_file]).split()[0])
count = 0

with open(feeds_file, 'r', encoding='UTF-8') as file:
   while line := file.readline():
      count += 1
      print(f"  **  Addign Feed {count} of {total}: {line}")
      add_feed(driver, rss_chanel_id, line, add_rss_submit_btn_id)

import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#initializing empty List and RegEx pattern
pattern = re.compile(r'(?<=v=)[^&]+')
v_id = []

header_list = []

Auth_Option = input("Is your 2-Auth enabled?(y/n) : \n")

#To disable safety feature for automation check
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

#Initiliazing the webdriver
webdriver = webdriver.Chrome(options = options)
webdriver.get('https://www.youtube.com/signin')
time.sleep(2)

username = webdriver.find_element(By.ID,'identifierId')
if (username) : 
    print('Found Username')
    username.send_keys('t2621814')
    username.send_keys(Keys.RETURN)
    time.sleep(3)
password = webdriver.find_element(By.CLASS_NAME,'whsOnd')
if (password):
    print('Found Password')
    password.send_keys('Test@123')
    password.send_keys(Keys.RETURN)
    if (Auth_Option == 'y' or Auth_Option == 'Y') :
        time.sleep(20)
    else :
        time.sleep(10)


webdriver.get("https://www.youtube.com/feed/history")
time.sleep(5)

last_height = webdriver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(3)

    # Calculate new scroll height and compare with last scroll height
    new_height = webdriver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(5)

days = webdriver.find_elements(By.TAG_NAME,'ytd-item-section-renderer')
for i in days : 
    time = i.find_elements(By.TAG_NAME,"ytd-video-renderer")
    for ti in time : 
        time = ti.find_element(By.ID,"thumbnail").find_element(By.CLASS_NAME,"badge-shape-wiz__text")
        print(time.text)
        
import json as js
import re
import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#initializing empty List and RegEx pattern
pattern = re.compile(r'(?<=v=)[^&]+')
time_pattern = re.compile(r"t=(\d+)s?")

#Auth Option to adopt to time delay
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
    username.send_keys('t2621814')
    username.send_keys(Keys.RETURN)
    time.sleep(3)
password = webdriver.find_element(By.CLASS_NAME,'whsOnd')
if (password):
    password.send_keys('Test@123')
    password.send_keys(Keys.RETURN)
    if (Auth_Option == 'y' or Auth_Option == 'Y') :
        time.sleep(20)
    else :
        time.sleep(10)


webdriver.get("https://www.youtube.com/feed/history")
time.sleep(7)

#TODO : Scroll dynamically down the page to load more videos
z = 0
while True :
    z += 1
    time.sleep(2)
    webdriver.execute_script('scrollBy(0,300)')
    if z > 4:
        break

data = {}
days = webdriver.find_elements(By.TAG_NAME, 'ytd-item-section-renderer')

for i in days:
    day = i.find_element(By.ID,"header").find_element(By.ID,"title")
    print(day.text)
    vv = []
    # addressing each 'Video' section
    videos = i.find_elements(By.TAG_NAME, 'ytd-video-renderer')
    for vid in videos :
        title = vid.find_element(By.ID, 'video-title')
        v_code = title.get_attribute('href')
        match_code = pattern.search(v_code)
        match = time_pattern.search(v_code)
        if match:
            t_value = match.group(1) 
            vv.append([match_code.group(),t_value])
        else :
            time_element = vid.find_element(By.ID,"thumbnail").find_element(By.ID,"overlays")
            vv.append([match_code.group(),time_element.text])
    data[day.text] = vv
webdriver.quit()

with open('data.json','w') as f:
    js.dump(data,f)


# v_codes = webdriver.find_elements(By.ID,'video-title')
# for i in v_codes : 
#     v_code = i.get_attribute('href')
#     match = pattern.search(v_code)
#     if match:
#         v_id.append(match.group())
#         print("Extracted value:", match.group())
#     else:
#         print("No match found.")


# href = v_code.get_attribute('href')
# print(href)



# history = webdriver.find_element(By.ID,'contentContainer').find_element(By.ID,'guide-content').find_element(By.ID,'guide-inner-content').find_element(By.ID,'guide-section').find_element(By.ID,'sections').find_element(By.ID,'items')

# href = history.find_element(By.TAG_NAME,'a').get_attribute('href')
# if (href) : 
#     print('Found History')
#     webdriver.get(href)
#     time.sleep(5)
#     print('History Page Opened')
    # print(webdriver.page_source)
    # webdriver.quit()
    # print('Quitting')
    # exit()
#Works for the pop up
# try:
#     # Adjust the selector based on your inspection of the popup
#     WebDriverWait(webdriver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, "selector_for_close_button"))).click()
# except Exception as e:
#     print("Popup not found or already closed")


# webdriver = webdriver.Chrome()
# webdriver.get('https://www.youtube.com/')

# sign_in = webdriver.find_element(By.CLASS_NAME,"yt-spec-touch-feedback-shape__stroke")
# if(sign_in) : 
#     print("Hogya!")
#     time.sleep(2)
#     sign_in.click()

# home = webdriver.find_element(By.)
# home.click()
# if (sign_in) : 
#     sign_in.click()
#     time.sleep(3)
#     print('Found Sign In')


# side_bar = webdriver.find_element(By.ID,'start').find_element(By.ID,"guide-button")
# if (side_bar) : 
#     print("Found Side Bar") 
#     side_bar.click()
#     time.sleep(6)


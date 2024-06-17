from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

webdriver = webdriver.Chrome(options = options)
webdriver.get('https://www.youtube.com/signin')
time.sleep(2)
username = webdriver.find_element(By.ID,'identifierId')
if (username) : 
    print('Found Username')
    username.send_keys('priyanshsaxena787')
    username.send_keys(Keys.RETURN)
    time.sleep(3)
password = webdriver.find_element(By.CLASS_NAME,'whsOnd')
if (password):
    print('Found Password')
    password.send_keys('BlackSheep12')
    password.send_keys(Keys.RETURN)
    time.sleep(10)
# side_bar = webdriver.find_element(By.ID,'start').find_element(By.ID,"guide-button")
# if (side_bar) : 
#     print("Found Side Bar") 
#     side_bar.click()
#     time.sleep(6)
webdriver.get("https://www.youtube.com/feed/history")
time.sleep(7)
count = 0
# while count < 5:


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


webdriver.quit()

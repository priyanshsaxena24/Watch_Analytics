import json 
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys

def run_selenium_task(username_input, password_input, auth_option):
    # initializing empty List and RegEx pattern
    pattern = re.compile(r'(?<=v=)[^&]+')
    time_pattern = re.compile(r"t=(\d+)s?")

    # To disable safety feature for automation check
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")  # Required for running as root on some systems
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable only for Windows OS
    options.add_argument("--window-size=1920x1080")  # Set window size

    webdriver_instance = webdriver.Chrome(options=options)

    webdriver_instance.get('https://www.youtube.com/signin')
    time.sleep(2)

    username_elem = webdriver_instance.find_element(By.ID, 'identifierId')
    if username_elem: 
        username_elem.send_keys(username_input)
        username_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    password_elem = webdriver_instance.find_element(By.ID, 'password').find_element(By.TAG_NAME, 'input')
    if password_elem:
        password_elem.send_keys(password_input)
        password_elem.send_keys(Keys.RETURN)

    if auth_option.lower() == 'yes':
        time.sleep(20)
    else:
        time.sleep(10)

    webdriver_instance.get("https://www.youtube.com/feed/history")
    time.sleep(7)

    scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = webdriver_instance.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 1
    while True: 
        # scroll one screen height each time
        webdriver_instance.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = webdriver_instance.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if screen_height * i > scroll_height:
            webdriver_instance.execute_script('scrollBy(0,500)')
            break 

    data = {}
    days = webdriver_instance.find_elements(By.TAG_NAME, 'ytd-item-section-renderer')

    for day_elem in days:
        day = day_elem.find_element(By.ID, "header").find_element(By.ID, "title")
        video_details_list = []
        # addressing each 'Video' section
        videos = day_elem.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        for vid in videos:
            video_detail = {}
            title = vid.find_element(By.ID, 'video-title')
            v_code = title.get_attribute('href')
            match_code = pattern.search(v_code)
            match_time = time_pattern.search(v_code)

            if match_code:
                video_detail['videoID'] = match_code.group()
            else: 
                video_detail['videoID'] = None
            
            if match_time:
                t_value = match_time.group(1)
                video_detail['watchTime'] = t_value
            else:
                # Find the time element differently if the regular expression didn't match
                time.sleep(1)
                time_element = vid.find_element(By.ID, "thumbnail").find_element(By.ID, "overlays")
                video_detail['watchTime'] = time_element.text
            
            # Append each video's details to the day's list
            video_details_list.append(video_detail)
        
        # Assign the list of videos to the corresponding day
        data[day.text] = video_details_list

    webdriver_instance.quit()

    with open('data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    # Read command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 ytLogging.py <username> <password> <auth_option>")
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
    auth_option = sys.argv[3]
    
    run_selenium_task(username, password, auth_option)

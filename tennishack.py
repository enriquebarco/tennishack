import os
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# load enviornmental variables
load_dotenv()
url = os.getenv("TENNISHACK_URL")
username_keys = os.getenv('TENNISHACK_USERNAME')
password_keys = os.getenv('TENNISHACK_PASSWORD')
booking_url = os.getenv('TENNISHACK_BOOKING_URL')
binary_location = os.getenv('GOOGLE_CHROME_BIN')

# make window max size, chrome settings to run headless on heroku
chrome_options = Options()
chrome_options.add_argument('--kiosk')
chrome_options.binary_location = binary_location
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

 # Get the current day of the week
today = datetime.datetime.now().strftime("%A")

# function to book a court dynamically depending on if it is thursday or friday
def book_court(driver, wait, today):
    if today == 'Thursday' or today == 'Friday':
        time = '10:00 PM'
        court_index = 2
    else:
        time = '7:00 PM'
        court_index = -1
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div')))
        court_list = driver.find_elements(By.XPATH, f"//*[text()='{time}']")
        court = court_list[court_index]
        if len(court_list) == 0:
            print("No available courts at the desired time.")
        else:
            print(f'Today is {today} and will book a court accordingly')
            driver.execute_script("arguments[0].click();", court)
            print('moved to booking date')
    except Exception as e:
        print(f'Error moving to booking date: {e}')
        driver.quit()

# load initial login page
try:
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    driver.get(url)
    print('page loaded')
except Exception as e:
    print(f'Error loading page: {e}')
    driver.quit()

# input login information
try:
    username_el = driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_UserName')
    password_el = driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_Password')
    login_button_el = driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_LoginButton')

    username_el.send_keys(username_keys)
    password_el.send_keys(password_keys)
    login_button_el.click()
    print('logged in')
except Exception as e:
    print(f'Error logining into page: {e}')
    driver.quit()

# navigate to tennis bookings post authentication
try:
    driver.get(booking_url)
    print('succesfully navigated to booking page')
except Exception as e:
    print(f'Error moving to booking url: {e}')

# show courts available two days ahead
try:
    wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element(By.XPATH,'//*[@id="module"]')))
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div')))
    two_days_advance_div = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div[4]')))
    driver.execute_script("arguments[0].click();", two_days_advance_div)
    print('navigated to correct date')
except Exception as e:
    print(f'Error navigating to correct booking date: {e}')
    driver.quit()

# book the court
book_court(driver, wait, today)

# complete booking
try:
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.content.row > div.col-xs-12.col-sm-7.section-2 > div > div.row > div > div > a")))
    book_button_el = driver.find_element(By.CSS_SELECTOR, "#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.content.row > div.col-xs-12.col-sm-7.section-2 > div > div.row > div > div > a")
    driver.execute_script("arguments[0].click();", book_button_el)

    # confirm booking
    confirmation = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[1]/h1')))

    if confirmation:
        print('booked!')
        driver.quit()

except Exception as e:
    print(f'Error booking court: {e}')
    driver.quit()


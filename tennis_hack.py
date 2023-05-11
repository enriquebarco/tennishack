import os
import datetime
import traceback
import base64
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# load enviornmental variables
url = os.environ["TENNISHACK_URL"]
username_keys = os.environ['TENNISHACK_USERNAME']
password_keys = os.environ['TENNISHACK_PASSWORD']
booking_url = os.environ['TENNISHACK_BOOKING_URL']

# make window max size, chrome settings to run headless on heroku
options = Options()
options.binary_location = '/opt/headless-chromium'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')

# Get the current day of the week
today = datetime.datetime.now().strftime("%A")

# function to book a court dynamically depending on if it is thursday or friday
def book_court(driver, wait, today):
    if today == 'Thursday' or today == 'Friday':
        # book court 3 at 10am
        time = '10:00 PM'
        court_index = 2
    else:
        # book court 7 at 7pm
        time = '7:00 PM'
        court_index = -1
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div')))
        court_list = driver.find_elements(By.XPATH, f"//*[text()='{time}']")
        court = court_list[court_index]
        if len(court_list) == 0:
            print("No available courts at the desired time.")
        else:
            if court_index >= len(court_list) or court_index < -len(court_list):
                print(f"Court index {court_index} is out of range for the available courts. Booking first available court instead.")
                court_index = 0  # fall back to the first available court
            court = court_list[court_index]
            print(f'Today is {today} and will book a court accordingly')
            driver.execute_script("arguments[0].click();", court)
            print('moved to booking date')
    except Exception as e:
        print(f'Error moving to booking date: {e}')
        driver.quit()

def main():
    # load initial login page
    try:
        driver = webdriver.Chrome('/opt/chromedriver', options=options)
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
        time.sleep(10)
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
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.header.row.mar-none > div.book-now.col-xs-8.text-right > a')))
        book_button_el = driver.find_element(By.CSS_SELECTOR, '#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.header.row.mar-none > div.book-now.col-xs-8.text-right > a')
        print('found button')
         # Save screenshot before click
        driver.save_screenshot('/tmp/before_click.png')
        with open('/tmp/before_click.png', 'rb') as file:
            before_click_b64 = base64.b64encode(file.read()).decode('utf-8')

        # Click the button
        driver.execute_script("arguments[0].click();", book_button_el)
        print('clicked book button')

        # Save screenshot after click
        driver.save_screenshot('/tmp/after_click.png')
        with open('/tmp/after_click.png', 'rb') as file:
            after_click_b64 = base64.b64encode(file.read()).decode('utf-8')
        
        print(before_click_b64)
        print(after_click_b64)

        # confirm booking
        confirmation_locator = (By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[1]/h1')
        confirmation = wait.until(EC.visibility_of_element_located(confirmation_locator))

        if confirmation:
            print('booked!')
            driver.quit()

    except Exception as e:
        print(f'Error: {e}\n{traceback.format_exc()}')
        driver.quit()  # Close the driver instance if it has been initialized

if __name__ == '__main__':
    main()

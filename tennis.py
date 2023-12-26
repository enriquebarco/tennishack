import os
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import handle_screenshot
from dotenv import load_dotenv

# load environmental variables
load_dotenv()

class TennisCourtBooking:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.today = datetime.datetime.now().strftime("%A")
        self.url = os.getenv("TENNISHACK_URL")
        self.booking_url = os.getenv('TENNISHACK_BOOKING_URL')
        self.username = os.getenv('TENNISHACK_USERNAME')
        self.password = os.getenv('TENNISHACK_PASSWORD')

    def login(self):
        try:
            self.driver.get(self.url)
            print('Page loaded')
            username_el = self.driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_UserName')
            password_el = self.driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_Password')
            login_button_el = self.driver.find_element(By.CSS_SELECTOR,'#p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_LoginButton')

            username_el.send_keys(self.username)
            password_el.send_keys(self.password)
            login_button_el.click()
            print('Logged in')
        except Exception as e:
            print(f'Error logging into page: {e}')
            handle_screenshot(self.driver)

    def navigate_to_booking_page(self):
        try:
            self.driver.get(self.booking_url)
            print('Successfully navigated to booking page')

            self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.driver.find_element(By.XPATH, '//*[@id="module"]')))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div')))
            two_days_advance_div = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div[4]')))
            self.driver.execute_script("arguments[0].click();", two_days_advance_div)
            print('Navigated to correct date')

        except Exception as e:
            print(f'Error moving to booking URL: {e}')
            handle_screenshot(self.driver)

    def book_tennis_court(self):
        court_name, time = self.determine_booking_details()
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div')))
            xpath_expression = f"//div[@class='court-col ng-scope'][.//div[@class='court-name ng-binding' and contains(text(), '{court_name}')]]//*[text()='{time}']"
            court_list = self.driver.find_elements(By.XPATH, xpath_expression)

            print(f'Found {len(court_list)} slots at {time} for {court_name}')

            if len(court_list) == 0:
                print(f"No available slots at {time} for {court_name}. Trying to book any available court at 7 PM.")
                self.book_any_available_court()
            else:
                self.select_and_book_court(court_list, court_name, time)
        except Exception as e:
            print(f'Error in booking process: {e}')
            handle_screenshot(self.driver)

    def determine_booking_details(self):
        if self.today in ['Thursday', 'Friday']:
            return "Court 4", "10:00 AM"
        else:
            return "Court 7", "7:00 PM"

    def book_any_available_court(self):
        any_court_xpath = "//div[@class='court-col ng-scope']//*[text()='7 PM']"
        any_court_list = self.driver.find_elements(By.XPATH, any_court_xpath)

        if len(any_court_list) == 0:
            print("No available courts at 7 PM.")
        else:
            any_court_slot = any_court_list[0]
            print(f'Booking an available court at 7 PM.')
            self.driver.execute_script("arguments[0].click();", any_court_slot)
            print('Moved to booking.')

    def select_and_book_court(self, court_list, court_name, time):
        court_slot = court_list[0]
        print(f'Today is {self.today}. Booking {court_name} at {time}.')
        self.driver.execute_script("arguments[0].click();", court_slot)
        print('Moved to booking date.')

    def complete_booking(self):
        print('navigating to booking page')
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.content.row > div.col-xs-12.col-sm-7.section-2 > div > div.row > div > div > a")))
        print('page loaded')
        book_button_el = self.driver.find_element(By.CSS_SELECTOR, "#form1 > div.inner-wrap > div.container.c-module > div > div > div > div.main-content.ng-scope > div > div.content.row > div.col-xs-12.col-sm-7.section-2 > div > div.row > div > div > a")
        print('found book button')
        self.driver.execute_script("arguments[0].click();", book_button_el)

        # confirm booking
        confirmation = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[1]/h1')))
        if confirmation:
            print('booked!')
            self.driver.quit()

    def run(self):
        self.navigate_to_booking_page()
        self.book_tennis_court()
        self.complete_booking()

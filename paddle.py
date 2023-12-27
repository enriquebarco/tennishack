import os
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from utils import handle_screenshot
from dotenv import load_dotenv

# load environmental variables
load_dotenv()

class PaddleCourtBooking:
    def __init__(self, driver, wait):
        self.retries = 0
        self.driver = driver
        self.wait = wait
        self.today = datetime.datetime.now().strftime("%A")
        self.url = os.getenv("PADDLE_URL")
        self.booking_url = os.getenv('PADDLE_BOOKING_URL')
        self.username = os.getenv('PADDLE_USERNAME')
        self.password = os.getenv('PADDLE_PASSWORD')
    
    def login(self):
        try:
            self.driver.get(self.url)
            print('Paddle page loaded')
            username_el = self.driver.find_element(By.CSS_SELECTOR,'#user_email')
            password_el = self.driver.find_element(By.CSS_SELECTOR,'#user_password')
            login_button_el = self.driver.find_element(By.CSS_SELECTOR,'#new_user > div > div > div.form-actions > input')

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

            two_days_advance_div = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.body_wrapper > div.pusher > div.yield_container.pb30 > div > div:nth-child(2) > div > div.ui.attached.segment > div > div:nth-child(1) > div.content.active > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div > div > button:nth-child(3)')))
            self.driver.execute_script("arguments[0].click();", two_days_advance_div)
            print('Navigated to correct date')

        except Exception as e:
            print(f'Error moving to booking URL: {e}')
            handle_screenshot(self.driver)
    
    def book_paddle_court(self):
        try:
            time_slots = ['7-7:30pm', '7:30-8pm', '8-8:30pm']
            for slot in time_slots:
                retry = 0
                while retry < 3:
                    try:
                        slot_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{slot}')]")))
                        self.driver.execute_script("arguments[0].click();", slot_element)
                        print(f'selected time slot {slot}')
                        break
                    except StaleElementReferenceException:
                        retry += 1
                        if retry >= 3:
                            print(f"Failed to select time slot {slot} after retries.")
                            raise

            # click next
            next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.body_wrapper > div.pusher > div.yield_container.pb30 > div > div:nth-child(2) > div > div.ui.attached.segment > div > div:nth-child(1) > div.content.active > table > tbody > tr > td:nth-child(2) > div.position_sticky_bottom_on_mobile.bk_white.mtb20.ptb10.z-index-1 > div.ui.buttons.fluid > button")))
            self.driver.execute_script("arguments[0].click();", next_button)
            print('clicked next')

        except Exception as e:
            print(f'Error selecting slots: {e}')
            handle_screenshot(self.driver)

    def confirm_booking(self):
            try:
                # click next
                next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.body_wrapper > div.pusher > div.yield_container.pb30 > div > div:nth-child(2) > div > div.ui.attached.segment > div > div:nth-child(2) > div.content.active > table > tbody > tr > td:nth-child(2) > div.position_sticky_bottom_on_mobile.bk_white.mtb20.ptb10.z-index-1 > div > button")))
                self.driver.execute_script("arguments[0].click();", next_button)
                print('clicked next, moving to final booking page')

                # click book
                book_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.body_wrapper > div.pusher > div.yield_container.pb30 > div > div:nth-child(2) > div > div.ui.attached.segment > div > div:nth-child(3) > div.content.active > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > div.no-border-top > div > div > div > button")))
                self.driver.execute_script("arguments[0].click();", book_button)
                print('clicked book button')

                confirmation = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.body_wrapper > div.pusher > div.yield_container.pb30 > div > div > div.ten.wide.computer.ten.wide.tablet.sixteen.wide.mobile.column.plr0_on_mobile > div.ui.segments.fluid.no_shadow_on_mobile > div:nth-child(1) > div.mtb10 > div > div:nth-child(2) > div > div.text.semi.black.bold')))

                if confirmation:
                    print('booked!')
                
            except Exception as e:
                print(f'Error confirming booking: {e}')
                handle_screenshot(self.driver)


    def run(self):
            while self.retries < 3:
                try:
                    self.navigate_to_booking_page()
                    self.book_paddle_court()
                    self.confirm_booking()
                    self.driver.quit()
                    break  # Exit loop if all steps are successful
                except Exception as e:
                    print(f'Error encountered: {e}. Retrying...')
                    self.retries += 1  # Increment retry count
                    if self.retries >= 3:
                        print("Maximum retries reached. Exiting.")
                        self.driver.quit()
                        break

            if self.retries < 3:
                print("Booking process completed successfully.")
            else:
                print("Booking process failed after maximum retries.")

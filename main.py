import os
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from tennis import TennisCourtBooking
from paddle import PaddleCourtBooking
from utils import wait_until_8am_est

# load enviornmental variables
load_dotenv()
binary_location = os.getenv('GOOGLE_CHROME_BIN')

# make window max size, chrome settings to run headless on heroku. To run localy, comment out chrome_options.binary_location and chrome_options.add_argument('--headless')
chrome_options = Options()
chrome_options.add_argument('--kiosk')
chrome_options.binary_location = binary_location
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

 # Get the current day of the week
today = datetime.datetime.now().strftime("%A")

def initialize_driver():
    chrome_options = Options()
    # Configure Chrome Options as needed
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    return driver, wait


def main ():
    driver, wait = initialize_driver()

    if today == 'Monday':
        paddle = PaddleCourtBooking(driver, wait)
        paddle.login()
        wait_until_8am_est()
        paddle.run()
    else:
        paddle = PaddleCourtBooking(driver, wait)
        paddle.login()
        wait_until_8am_est()
        paddle.run()
        tennis = TennisCourtBooking(driver, wait)
        tennis.login()
        wait_until_8am_est()
        tennis.run()


if __name__ == "__main__":
    main()
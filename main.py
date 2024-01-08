import os
import sys
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium_stealth import stealth
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

# act like a user
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
chrome_options.add_argument('--accept-language=en-US,en;q=0.5')
chrome_options.add_argument('--referer=https://www.google.com/')



 # Get the current day of the week
today = datetime.datetime.now().strftime("%A")

def initialize_driver():
    chrome_options = Options()
    # Configure Chrome Options as needed
    driver = webdriver.Chrome(options=chrome_options)

    # Apply stealth settings to the driver
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    wait = WebDriverWait(driver, 30)
    return driver, wait


def main ():
    if today == 'Tuseday':
        sys.exit('No bookings on Tuesdays')
        
    driver, wait = initialize_driver()

    if today == 'Monday':
        paddle = PaddleCourtBooking(driver, wait)
        paddle.login()
        wait_until_8am_est()
        paddle.run()
    else:
        tennis = TennisCourtBooking(driver, wait)
        tennis.login()
        wait_until_8am_est()
        tennis.run()


if __name__ == "__main__":
    main()
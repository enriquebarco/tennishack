import os
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
chrome_driver_path = os.getenv('CHROMEDRIVER_PATH')

# make window max size
chrome_options = Options()
chrome_options.add_argument('--kiosk')
chrome_options.binary_location = binary_location
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# load initial login page
driver = webdriver.Chrome(executable_path=chrome_driver_path,  options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)
driver.get(url)

# input login information
username_el = driver.find_element(By.XPATH,'//*[@id="p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_UserName"]')
password_el = driver.find_element(By.XPATH,'//*[@id="p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_Password"]')
login_button_el = driver.find_element(By.XPATH,'//*[@id="p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_LoginButton"]')

username_el.send_keys(username_keys)
password_el.send_keys(password_keys)
login_button_el.click()

print('logged in')

# navigate to tennis bookings post authentication
driver.get(booking_url)

# show courts available two days ahead
wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element(By.XPATH,'//*[@id="module"]')))
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div')))
two_days_advance_div = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div[4]')))
driver.execute_script("arguments[0].click();", two_days_advance_div)

print('navigated to correct date')

# select court available at 7pm
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div')))
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div/div[6]/div/div/div[2]')))
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[5]/div[1]/div/div/div/div[6]/div/div/div[2]/div[18]')))
court = driver.find_element(By.XPATH, "//*[text()='7:00 PM']")
driver.execute_script("arguments[0].click();", court)

print('moved to booking date')

# complete booking
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/div/div/div/div[3]/div/div[3]/div[2]')))
book_button_el = driver.find_element(By.XPATH,'//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[3]/div[2]/div/div[2]/div/div/a')
driver.execute_script("arguments[0].click();", book_button_el)

# confirm booking
confirmation = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div/div/div[3]/div/div[1]/h1')))

if confirmation:
    print('booked!')




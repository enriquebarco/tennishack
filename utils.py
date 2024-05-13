import datetime
import time
import pytz

def handle_screenshot(driver):
    base64_image = driver.get_screenshot_as_base64()
    print(base64_image)

import datetime
import time
import pytz  # You need to install this package for timezone handling

def wait_until_8am_est():
    # Timezone for Eastern Time
    eastern = pytz.timezone('America/New_York')

    # Current time in UTC
    now_utc = datetime.datetime.now(pytz.utc)
    print(f"Function start time (UTC): {now_utc}")

    # Convert current UTC time to Eastern Time
    now_est = now_utc.astimezone(eastern)

    # Set target time as 9:10 PM Eastern Time today
    target_time_est_today = now_est.replace(hour=8, minute=0, second=0, microsecond=500000)

    # If current Eastern Time is past the target, log and return
    if now_est > target_time_est_today:
        print("Target time has already passed. Ending function.")
        return

    # Convert target Eastern Time back to UTC
    target_time_utc = target_time_est_today.astimezone(pytz.utc)

    print(f"Target time in EST/EDT: {target_time_est_today}")

    # Calculate sleep time
    time_to_sleep = (target_time_utc - now_utc).total_seconds() - 5  # Wake up 10 seconds before the target time
    print(f"Sleeping for {max(time_to_sleep, 0)} seconds...")
    time.sleep(max(time_to_sleep, 0))

    # Final check loop to synchronize precisely with 9:10 PM EST/EDT
    print(f'Waking up...{target_time_est_today}')
    while datetime.datetime.now(pytz.utc) < target_time_utc:
        pass 

    print(f"It is now: {datetime.datetime.now(pytz.utc)}, which is equivalent to {target_time_est_today} EST/EDT. Continuing script...")


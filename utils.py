
def handle_screenshot(driver):
    base64_image = driver.get_screenshot_as_base64()
    print(base64_image)
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MY_EMAIL = "********************"
MY_PASSWORD = "*****************"
TINDER_URL = "https://tinder.com/"
DEFAULT_TIMEOUT_SECONDS = 15


def create_driver():
    """Create browser instance with undetected_chromedriver."""
    return uc.Chrome()


def wait_for(driver, condition, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Helper for explicit waits."""
    return WebDriverWait(driver, timeout).until(condition)


def click_login_on_home(driver):
    """Click the homepage 'Log in' button."""
    login_buttons = driver.find_elements(By.CLASS_NAME, "c1p6lbu0")
    for item in login_buttons:
        if item.text.strip().lower() == "log in":
            item.click()
            return
    raise RuntimeError("Could not find Tinder 'Log in' button.")


def login_with_google(driver, email, password):
    """Run Google login flow from Tinder modal.

    Example:
    login_with_google(driver, "you@example.com", "your-password")
    """
    wait_for(driver, EC.presence_of_element_located((By.ID, "q494877495"))).click()

    wait_for(driver, lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])

    username = wait_for(driver, EC.presence_of_element_located((By.NAME, "identifier")))
    username.send_keys(email)
    wait_for(driver, EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-k8QpJ"))).click()

    password_input = wait_for(driver, EC.presence_of_element_located((By.NAME, "Passwd")))
    password_input.send_keys(password)
    wait_for(driver, EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-k8QpJ"))).click()

    input("Complete any Google/Tinder 2FA in browser, then press Enter...")


def main():
    driver = create_driver()
    driver.get(TINDER_URL)

    try:
        time.sleep(3)
        click_login_on_home(driver)
        time.sleep(3)
        login_with_google(driver, MY_EMAIL, MY_PASSWORD)
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
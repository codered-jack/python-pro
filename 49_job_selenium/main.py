from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

MY_EMAIL = "********************"
MY_PASSWORD = "*****************"
LINKEDIN_JOBS_URL = (
    "https://www.linkedin.com/jobs/search/?currentJobId=3362855988&f_AL=true&f_WT=2"
    "&geoId=103121230&keywords=python%20developer&location=Philippines&refresh=true"
)
SHORT_WAIT_SECONDS = 2
PAGE_LOAD_WAIT_SECONDS = 5


def wait(seconds=SHORT_WAIT_SECONDS):
    """Small helper to make selenium steps easier to read."""
    time.sleep(seconds)


def login(driver, email, password):
    """Login to LinkedIn from jobs page."""
    sign_in_webpage = driver.find_element(By.LINK_TEXT, "Sign in")
    sign_in_webpage.click()

    linkedin_signin_window = driver.window_handles[0]
    driver.switch_to.window(linkedin_signin_window)

    username = driver.find_element(By.ID, "username")
    username.send_keys(email)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    signin_button = driver.find_element(By.CLASS_NAME, "btn__primary--large")
    signin_button.click()
    wait(PAGE_LOAD_WAIT_SECONDS)


def close_easy_apply_modal(driver):
    """Close easy apply modal and discard draft if asked."""
    close_easyapp_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
    close_easyapp_button.click()
    wait()
    dismiss_button = driver.find_element(
        By.CSS_SELECTOR,
        '[data-control-name="discard_application_confirm_btn"]',
    )
    dismiss_button.click()


def save_job(driver):
    """Click save button on current job and close toast if shown."""
    save_button = driver.find_element(By.CLASS_NAME, "jobs-save-button")
    save_button.click()
    wait(PAGE_LOAD_WAIT_SECONDS)
    try:
        close_popup = driver.find_element(By.CSS_SELECTOR, ".artdeco-toast-item__dismiss")
        close_popup.click()
    except NoSuchElementException:
        pass


def follow_company(driver):
    """Scroll near footer and click follow button."""
    locate_follow_section = driver.find_element(By.CSS_SELECTOR, ".jobs-company__footer")
    ActionChains(driver).move_to_element(locate_follow_section).perform()
    wait()
    get_follow_button = driver.find_element(By.CSS_SELECTOR, ".follow")
    get_follow_button.click()


def process_job(driver, job):
    """Process one job card:
    - if single-step easy apply exists: save + follow
    - if multi-step: skip and discard
    """
    job.click()
    wait(3)

    find_easy_apply = driver.find_element(By.CLASS_NAME, "jobs-apply-button--top-card")
    find_easy_apply.click()

    try:
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Submit application"]')
        close_easy_apply_modal(driver)
        save_job(driver)
        follow_company(driver)
    except NoSuchElementException:
        print("There are too many steps to this application. Don't save and skip to next job.")
        close_easy_apply_modal(driver)


def main():
    driver = webdriver.Chrome()
    driver.get(LINKEDIN_JOBS_URL)
    driver.maximize_window()

    try:
        login(driver, MY_EMAIL, MY_PASSWORD)
        all_jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
        for job in all_jobs:
            process_job(driver, job)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

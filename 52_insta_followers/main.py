from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


SIMILAR_ACCOUNT = "selfcareisforeveryone"
USERNAME = ""
PASSWORD = ""
BASE_URL = "https://www.instagram.com"
FOLLOW_SCROLL_ROUNDS = 5
BUTTON_CLICK_DELAY_SECONDS = 2

class Instafollower:
    def __init__(self) -> None:
        # Cross-platform: Selenium Manager resolves the right driver automatically.
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)


    def login(self):
        """Login to Instagram with configured credentials."""
        self.driver.get(f"{BASE_URL}/")

        username = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(USERNAME)

        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)

        time.sleep(10)
    
    def find_followers(self):
        """Open target account followers popup.

        Example target URL:
        https://www.instagram.com/selfcareisforeveryone/
        """
        self.driver.get(f"{BASE_URL}/{SIMILAR_ACCOUNT}/")
        time.sleep(3)
        followers = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[href="/{SIMILAR_ACCOUNT}/followers/"]'))
        )
        followers.click()
        time.sleep(5)

    def follow(self):
        """Follow visible users, then scroll and repeat."""
        # Followers modal scroll container class can change over time.
        # This selector works for this course snapshot.
        follower_names = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._aano"))
        )

        for _ in range(FOLLOW_SCROLL_ROUNDS):
            follow_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Follow']")
            for button in follow_buttons:
                try:
                    button.click()
                    time.sleep(BUTTON_CLICK_DELAY_SECONDS)
                except Exception:
                    continue

            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                follower_names,
            )
            time.sleep(2)

        time.sleep(40)
    
    def close(self):
        self.driver.quit()


def main():
    instagram = Instafollower()
    try:
        instagram.login()
        instagram.find_followers()
        instagram.follow()
    finally:
        instagram.close()


if __name__ == "__main__":
    main()
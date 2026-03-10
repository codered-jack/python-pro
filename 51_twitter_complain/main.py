import time

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = "************"
TWITTER_PASSWORD = "************"
TWITTER_USERNAME = "************"  # Used if Twitter asks for extra verification.
SPEEDTEST_WAIT_SECONDS = 70
TWITTER_LOAD_WAIT_SECONDS = 35


class InternetSpeedTwitterBot:
    """Measures internet speed and tweets complaint if under promised values.

    Example flow:
    1) bot.get_internet_speed()
    2) bot.twitter_login(TWITTER_EMAIL)
    3) bot.tweet_at_provider(TWITTER_PASSWORD, message)
    """

    def __init__(self):
        self.promised_down = PROMISED_DOWN
        self.promised_up = PROMISED_UP
        self.driver = uc.Chrome()
        self.download = 0.0
        self.upload = 0.0

    def get_internet_speed(self):
        """Run speedtest and build tweet message."""
        self.driver.get("https://www.speedtest.net/")
        self.driver.find_element(By.CLASS_NAME, "js-start-test").click()

        time.sleep(SPEEDTEST_WAIT_SECONDS)
        results = self.driver.find_elements(By.CLASS_NAME, "result-data")

        self.download = float(results[3].text)
        self.upload = float(results[4].text)
        return (
            f"Hey Internet Provider, why is my internet speed {self.download} down/"
            f"{self.upload} up when I pay for {self.promised_down} down/{self.promised_up} up?"
        )

    def twitter_login(self, email):
        """Login with Twitter email-first flow."""
        self.driver.get("https://twitter.com")
        time.sleep(TWITTER_LOAD_WAIT_SECONDS)

        self.driver.find_element(By.CSS_SELECTOR, '[href="/login"]').click()
        time.sleep(5)

        login = self.driver.find_element(By.NAME, "text")
        login.send_keys(email)
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/"
            "div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]",
        ).click()
        time.sleep(10)

    def tweet_at_provider(self, password, message):
        """Send complaint tweet after login."""
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/"
            "div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div",
        ).click()

        time.sleep(15)
        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Tweet"]').click()
        time.sleep(5)

        write_tweet = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-ltr")
        write_tweet.send_keys(message)
        self.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]').click()

    def unusual_login(self, twitter_user):
        """Handle additional username challenge if Twitter requests it."""
        unusual_login_alert = self.driver.find_element(By.NAME, "text")
        unusual_login_alert.send_keys(twitter_user)
        unusual_login_alert.send_keys(Keys.ENTER)

    def close(self):
        self.driver.quit()


def main():
    bot = InternetSpeedTwitterBot()
    try:
        tweet_message = bot.get_internet_speed()
        bot.twitter_login(TWITTER_EMAIL)
        try:
            bot.tweet_at_provider(TWITTER_PASSWORD, tweet_message)
        except NoSuchElementException:
            bot.unusual_login(TWITTER_USERNAME)
            time.sleep(6)
            bot.tweet_at_provider(TWITTER_PASSWORD, tweet_message)
    finally:
        time.sleep(3)
        bot.close()


if __name__ == "__main__":
    main()

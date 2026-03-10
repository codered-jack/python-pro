# Exercise 1
# Challenge: Use Selenium to scrape website data.
#
# Example output format:
# {
#   0: {"time": "2026-02-27", "name": "PyCon 2026"},
#   1: {"time": "2026-03-04", "name": "DjangoCon Europe"},
#   ...
# }

from selenium import webdriver
from selenium.webdriver.common.by import By

PYTHON_HOME_URL = "https://www.python.org/"


def extract_upcoming_events(driver):
    """Return Python.org upcoming events as an indexed dictionary."""
    date_elements = driver.find_elements(By.CSS_SELECTOR, ".event-widget ul.menu time")
    name_elements = driver.find_elements(By.CSS_SELECTOR, ".event-widget ul.menu a")

    dates = [date.text for date in date_elements]
    names = [name.text for name in name_elements]

    events = {}
    for index, (date, name) in enumerate(zip(dates, names)):
        events[index] = {"time": date, "name": name}

    return events


def main():
    # Selenium Manager can auto-resolve the browser driver in modern Selenium.
    driver = webdriver.Chrome()
    try:
        driver.get(PYTHON_HOME_URL)
        upcoming_events = extract_upcoming_events(driver)
        print(upcoming_events)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
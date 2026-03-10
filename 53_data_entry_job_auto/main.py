from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64481581640625%2C%22east%22%3A-122.22184218359375%2C%22south%22%3A37.64220115428586%2C%22north%22%3A37.908142595089714%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
GOOGLE_FORM_URL = "MY GOOGLE FORM ADDRESS LINK"
FORM_LOAD_WAIT_SECONDS = 2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "upgrade-insecure-requests": "1",
}


def fetch_zillow_html():
    """Fetch Zillow listings page HTML."""
    response = requests.get(ZILLOW_URL, headers=headers)
    response.raise_for_status()
    return response.text


def parse_property_data(html):
    """Extract addresses, prices, and links from Zillow HTML.

    Example return:
    (
        ["123 Main St, ...", "456 Pine St, ..."],
        ["$2,900", "$2,450"],
        ["https://www.zillow.com/...", "https://www.zillow.com/..."]
    )
    """
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class": "property-card-link"})
    all_property_links = [link.get("href") for link in links if link.get("href")]
    new_property_links = [
        link if link.startswith("https://www.zillow.com") else f"https://www.zillow.com{link}"
        for link in all_property_links
    ]

    all_prices = soup.find_all("div", {"class": "StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0"})
    price_list = [item.text for price in all_prices for item in price.find_all("span")]
    prices = [price.replace("/", "+").split("+")[0].strip() for price in price_list]

    find_addresses = soup.find_all(name="address")
    addresses = [adds.text.strip() for adds in find_addresses]

    # Align lengths to avoid index errors if scrape counts differ.
    min_len = min(len(addresses), len(prices), len(new_property_links))
    return addresses[:min_len], prices[:min_len], new_property_links[:min_len]


def fill_google_form(addresses, prices, links):
    """Submit one form response per property listing."""
    # Cross-platform: Selenium Manager resolves the right driver automatically.
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        for address, price, link in zip(addresses, prices, links):
            driver.get(GOOGLE_FORM_URL)
            time.sleep(FORM_LOAD_WAIT_SECONDS)

            google_form = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf"))
            )
            google_form[0].send_keys(address)
            google_form[1].send_keys(price)
            google_form[2].send_keys(link)

            submit_button = driver.find_element(By.CSS_SELECTOR, '[jsname="M2UYVd"]')
            submit_button.click()
            time.sleep(2)
    finally:
        driver.quit()


def main():
    zillow_page = fetch_zillow_html()
    addresses, prices, links = parse_property_data(zillow_page)
    fill_google_form(addresses, prices, links)


if __name__ == "__main__":
    main()
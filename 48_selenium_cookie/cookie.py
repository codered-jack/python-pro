from selenium import webdriver
from selenium.webdriver.common.by import By
import time

COOKIE_URL = "http://orteil.dashnet.org/experiments/cookie/"
CHECK_INTERVAL_SECONDS = 5
RUN_DURATION_SECONDS = 60 * 5


def get_store_item_ids(driver):
    """Get upgrade item IDs in store order.

    Example:
    ["buyCursor", "buyGrandma", "buyFactory", ...]
    """
    products = driver.find_elements(By.CSS_SELECTOR, "#store div")
    return [product.get_attribute("id") for product in products if product.get_attribute("id")]


def get_item_prices(driver):
    """Get current store prices parsed as integers."""
    product_prices = []
    products = driver.find_elements(By.CSS_SELECTOR, "#store b")
    for product in products:
        # Example product text: "Cursor - 15"
        price_text = product.text.split("-")[-1].replace(",", "").strip()
        if price_text:
            product_prices.append(int(price_text))
    return product_prices


def get_cookie_money(driver):
    """Read current cookie balance as integer."""
    money_text = driver.find_element(By.ID, "money").text.replace(",", "")
    return int(money_text)


def choose_best_affordable_item(catalogue, cookie_money):
    """Return the most expensive item you can currently afford."""
    affordable = {item_id: price for item_id, price in catalogue.items() if price <= cookie_money}
    if not affordable:
        return None

    # Pick by price, not by item id.
    return max(affordable, key=affordable.get)


def main():
    driver = webdriver.Chrome()
    driver.get(COOKIE_URL)

    cookie = driver.find_element(By.ID, "cookie")
    all_products = get_store_item_ids(driver)
    print(all_products)

    next_check = time.time() + CHECK_INTERVAL_SECONDS
    end_time = time.time() + RUN_DURATION_SECONDS

    while True:
        cookie.click()

        if time.time() > next_check:
            product_prices = get_item_prices(driver)
            cookie_money = get_cookie_money(driver)

            product_catalogue = dict(zip(all_products, product_prices))
            best_item_id = choose_best_affordable_item(product_catalogue, cookie_money)

            if best_item_id is not None:
                driver.find_element(By.ID, best_item_id).click()

            next_check = time.time() + CHECK_INTERVAL_SECONDS

        if time.time() > end_time:
            cookies_per_second = driver.find_element(By.ID, "cps")
            print(f"Cookies per second: {cookies_per_second.text}")
            break

    driver.quit()


if __name__ == "__main__":
    main()
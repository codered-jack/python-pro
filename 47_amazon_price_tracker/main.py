from bs4 import BeautifulSoup
import requests
import smtplib

MY_EMAIL = "**************"
MY_PASSWORD = "************"
TARGET_PRICE = 100

AMAZON_URL = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=sr_1_5?crid=1HBIPQA988RCO&keywords=instant+pot+duo+evo&qid=1673901445&s=home-garden&sprefix=instant+pot+%2Cgarden%2C2424&sr=1-5"

amazon_headers = {
    "Accept-Language": "en-US,en;q=0.9,fil;q=0.8,fr;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}


def fetch_product_page(url, headers):
    """Fetch Amazon product page HTML."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_price(price_text):
    """Convert raw Amazon price text to float.

    Example:
    "$129.99" -> 129.99
    """
    cleaned_price = price_text.replace("$", "").replace(",", "").strip()
    return float(cleaned_price)


def parse_product_details(html):
    """Extract product title and current visible price from HTML.

    Example return:
    ("Instant Pot Duo ...", 129.99)
    """
    soup = BeautifulSoup(html, "lxml")

    product_name = soup.select_one("#productTitle").get_text(strip=True)

    # Use offscreen price for reliable numeric text (e.g., "$129.99").
    product_price_tag = soup.select_one("span.a-price span.a-offscreen")
    if product_price_tag is None:
        raise ValueError("Could not find product price on page.")

    price_value = parse_price(product_price_tag.get_text())
    return product_name, price_value


def send_price_alert(message):
    """Send email alert when product goes below target price."""
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price alert! \n\n{message}.".encode("UTF-8"),
        )


def main():
    product_page = fetch_product_page(AMAZON_URL, amazon_headers)
    product_name, current_price = parse_product_details(product_page)

    message = f"{product_name} is now ${current_price}. See {AMAZON_URL}"

    if current_price < TARGET_PRICE:
        send_price_alert(message)


if __name__ == "__main__":
    main()
import os
import requests

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "insert id")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "add your token")
ALPHAVANTAGE_API = os.getenv("ALPHAVANTAGE_API", "add your api")
NEWS_API = os.getenv("NEWS_API", "add your api")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHAVANTAGE_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

THRESHOLD_PERCENT = 5
NEWS_LIMIT = 3
REQUEST_TIMEOUT = 20


def get_stocks():
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "apikey": ALPHAVANTAGE_API,
    }
    response = requests.get(ALPHAVANTAGE_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Unexpected AlphaVantage response: {data}")

    return data["Time Series (Daily)"]


def get_news(from_date: str, to_date: str):
    params = {
        "qInTitle": COMPANY_NAME,
        "from": from_date,   # older date
        "to": to_date,       # newer date
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": NEWS_LIMIT,
        "apiKey": NEWS_API,
    }
    response = requests.get(NEWS_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    if "articles" not in data:
        raise ValueError(f"Unexpected NewsAPI response: {data}")

    return data["articles"]


def send_telegram_message(message: str):
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(TELEGRAM_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_last_two_trading_days(stocks: dict):
    # API keys are date strings like "2026-03-06", newest first
    sorted_dates = sorted(stocks.keys(), reverse=True)
    if len(sorted_dates) < 2:
        raise ValueError("Not enough stock data to compare two days.")
    return sorted_dates[0], sorted_dates[1]


def main():
    stocks = get_stocks()
    latest_date, previous_date = get_last_two_trading_days(stocks)

    latest_close = float(stocks[latest_date]["4. close"])
    previous_close = float(stocks[previous_date]["4. close"])

    price_diff = latest_close - previous_close
    percent_diff = abs((price_diff / previous_close) * 100)
    direction = "UP" if price_diff > 0 else "DOWN"

    if percent_diff < THRESHOLD_PERCENT:
        send_telegram_message(
            f"{STOCK}: No significant change ({percent_diff:.2f}%) between {previous_date} and {latest_date}."
        )
        return

    # Pull news for the comparison window
    articles = get_news(from_date=previous_date, to_date=latest_date)

    if not articles:
        send_telegram_message(
            f"{STOCK} {direction} {percent_diff:.2f}%\nNo related news found."
        )
        return

    for article in articles[:NEWS_LIMIT]:
        title = article.get("title", "No title")
        brief = article.get("description", "No description")
        url = article.get("url", "")
        message = (
            f"{STOCK} {direction} {percent_diff:.2f}%\n"
            f"Headline: {title}\n"
            f"Brief: {brief}\n"
            f"Link: {url}"
        )
        send_telegram_message(message)


if __name__ == "__main__":
    main()
import requests
import smtplib

TELEGRAM_CHAT_ID = "*******"
TELEGRAM_TOKEN = "***********************************"

MY_EMAIL = "*************"
MY_PASSWORD = "**************"


class NotificationManager:
    # This class is responsible for sending notifications with deal details.

    def send_telegram_message(self, message):
        # Example final URL (conceptually):
        # https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>&text=Low%20price...
        parameters = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        }

        response = requests.post(url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params=parameters)
        response.raise_for_status()
        data = response.json()
        return data

    def send_emails(self, message, customer_email):
        """This emails the customers in sheety spreadsheet"""
        # Example:
        # send_emails("Low price alert! ...", "john@example.com")
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=customer_email,
                msg=f"Subject:Cheap Airfare Alert!\n\n{message}\n".encode('utf-8'))
import requests

TELEGRAM_CHAT_ID = "************"
TELEGRAM_TOKEN = "************************************"


class NotificationManager:

    def send_telegram_message(self, message):
        """ This sends a notification with a deal to Telegram. """
        # Example final URL (conceptually):
        # https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>&text=Low%20price...
        # Example message:
        # "Low price alert! Only Gbp 89 to fly from London-Paris to LON-PAR..."
        parameters = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        }

        response = requests.post(url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params=parameters)
        response.raise_for_status()
        data = response.json()
        # Example Telegram response (simplified):
        # {"ok": True, "result": {"message_id": 123, "chat": {"id": 999}}}
        return data

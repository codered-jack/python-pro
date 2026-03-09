from customers import get_customer_email
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


flights = FlightSearch()
managed_data = DataManager()
notify = NotificationManager()


SHEETY_URL = 'https://api.sheety.co/<addSHEETYURL>'

sheet_data = managed_data.get_sheet_data(SHEETY_URL, sheet_key="prices")

# Look for IATA Codes
# sheet_data = flights.search_iata_code(sheet_data)
# pprint(sheet_data)

# Put IATA Codes in Sheety
# managed_data.add_iatacode_to_sheet(SHEETY_URL, sheet_data)


# Search for Cheap Flights and send notification

DEPART_FROM = "LON"
stopovers = 0

def alert_customer(price, departure_city, arrival_city, depart_iata, arrive_iata, outbound, inbound):
    """Build deal alert text with a Google Flights deep link.

    Example:
    alert_customer(89, "London", "Paris", "LON", "PAR", "2026-03-03", "2026-03-10")
    """
    alert = f"Low price alert! Only Gbp £{price} to fly from " \
            f"{departure_city}-{arrival_city} to {depart_iata}-{arrive_iata}, from {outbound} to " \
            f"{inbound} Link: https://www.google.co.uk/flights?hl=en#flt=" \
            f"{depart_iata}.{arrive_iata}.{outbound}*{arrive_iata}.{depart_iata}.{inbound}"
    return alert


def send_email_alerts(message):
    """Send one alert message to all customers returned by Sheety."""
    for customer in get_customer_email():
        notify.send_emails(message, customer["email"])


for item in sheet_data:
    used_stopovers = stopovers

    # Try direct flights first.
    all_available_flights = flights.search_cheap_flights(
        DEPART_FROM,
        item['iataCode'],
        stopovers,
    )

    # If no direct result, retry allowing up to 2 stopovers.
    if all_available_flights is None:
        all_available_flights = flights.search_cheap_flights(
            DEPART_FROM,
            item['iataCode'],
            stopovers=2,
        )
        used_stopovers = 2
        if all_available_flights is None:
            continue

    if item['lowestPrice'] > all_available_flights.price:
        message = alert_customer(
            all_available_flights.price,
            all_available_flights.departure_city_name,
            all_available_flights.arrival_city_name,
            all_available_flights.departure_airport_iata_code,
            all_available_flights.arrival_airport_iata_code,
            all_available_flights.outbound_date,
            all_available_flights.inbound_date,
        )
        send_email_alerts(message)
        # Keep original behavior: telegram is sent for fallback (stopover) alerts.
        if used_stopovers > 0:
            notify.send_telegram_message(message)
    else:
        print(
            f"A flight to {all_available_flights.arrival_city_name} is "
            f"{all_available_flights.price}. That's too expensive"
        )
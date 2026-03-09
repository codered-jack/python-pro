# Day39 - Flight Deal Finder (Project Flow)

This project checks flight prices and sends a Telegram alert when a cheaper deal is found.

## Files and Responsibility

- `main.py`: orchestrates the whole flow.
- `data_manager.py`: reads and updates destination rows in Sheety.
- `flight_search.py`: talks to Kiwi Tequila API for IATA and flight prices.
- `flight_data.py`: structured model for one flight result (`FlightData`).
- `notification_manager.py`: sends Telegram bot messages.

## End-to-End Flow

1. Load destination rows from Sheety.
2. Fill missing `iataCode` values using Tequila location lookup.
3. Push updated IATA codes back to Sheety.
4. For each destination:
   - Search cheapest round-trip flight from `LON`.
   - Compare returned price with `lowestPrice` from Sheety.
   - If current price is lower, send Telegram alert.
5. Print logs for both "deal found" and "too expensive" paths.

## ASCII Data Flow Diagram

```text
               +----------------------+
               |      main.py         |
               | (control/orchestration)
               +----------+-----------+
                          |
                          v
                +---------+----------+
                |   DataManager      |
                | get_sheet_data()   |
                +---------+----------+
                          |
                          v
             Sheety rows (city, iataCode, lowestPrice, id)
                          |
                          v
                +---------+----------+
                |   FlightSearch     |
                | search_iata_code() |
                +---------+----------+
                          |
                          v
              Missing iataCode resolved via Tequila API
                          |
                          v
                +---------+----------+
                |   DataManager      |
                | add_iatacode...    |
                +---------+----------+
                          |
                          v
                +---------+----------+
                |   FlightSearch     |
                | search_cheap_...   |
                +---------+----------+
                          |
                          v
                   FlightData (price, route, dates)
                          |
                          v
               Compare with lowestPrice in Sheety
                   /                     \
          price lower                   not lower
              |                            |
              v                            v
   +----------+-----------+          print "too expensive"
   | NotificationManager  |
   | send_telegram...     |
   +----------------------+
```

## Example Data Shapes

Sheety row:

```python
{
    "id": 2,
    "city": "Paris",
    "iataCode": "PAR",
    "lowestPrice": 54
}
```

FlightData object:

```python
FlightData(
    price=89,
    departure_city_name="London",
    departure_airport_iata_code="LON",
    arrival_city_name="Paris",
    arrival_airport_iata_code="PAR",
    outbound_date="2026-03-03",
    inbound_date="2026-03-10",
)
```

## Quick Run Checklist

- Add valid credentials/endpoints in:
  - `SHEETY_URL` (`main.py`)
  - `TEQ_API_KEY` (`flight_search.py`)
  - `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` (`notification_manager.py`)
- Run:

```bash
python3 main.py
```

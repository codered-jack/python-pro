# Day40 - Flight Club (Flow)

Day40 extends Day39 by adding customer subscriptions and email alerts.

## End-to-End Flow

1. Load destination rows from Sheety (`prices` sheet).
2. For each destination, search direct flight (`stopovers=0`).
3. If not found, retry with connecting flights (`stopovers=2`).
4. Compare found price with `lowestPrice` in sheet.
5. If cheaper:
   - Build alert message with Google Flights link.
   - Send email to all subscribed customers.
   - Send Telegram message.

## Example Data

Destination row:

```python
{"id": 2, "city": "Paris", "iataCode": "PAR", "lowestPrice": 54}
```

Customer row:

```python
{"firstName": "John", "lastName": "Doe", "email": "john@example.com"}
```

## Run

```bash
python3 main.py
```

To add a new customer interactively:

```bash
python3 customers.py
```

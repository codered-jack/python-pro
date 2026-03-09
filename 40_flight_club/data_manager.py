import requests


class DataManager:
    def get_sheet_data(self, url, sheet_key="prices"):
        """Fetch rows from Sheety.

        Example response shape:
        {
            "prices": [
                {"id": 2, "city": "Paris", "iataCode": "PAR", "lowestPrice": 54}
            ]
        }
        """
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()[sheet_key]

    def add_iatacode_to_sheet(self, url, sheety):
        """This function adds the iataCode to the Google sheet."""
        last_response = None

        for city in sheety:
            new_url = f"{url}/{city['id']}"
            flight_codes = {
                "price": {
                    "iataCode": city['iataCode'],
                }
            }
            # Example payload:
            # {"price": {"iataCode": "PAR"}}
            last_response = requests.put(url=new_url, json=flight_codes)
            last_response.raise_for_status()

        return last_response

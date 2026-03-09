import requests


class DataManager:
    def get_sheet_data(self, url):
        """Fetch destination rows from Sheety.

        Example response shape:
        {
            "sheet1": [
                {"id": 2, "city": "Paris", "iataCode": "", "lowestPrice": 54},
                {"id": 3, "city": "Berlin", "iataCode": "BER", "lowestPrice": 42}
            ]
        }
        """
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()["sheet1"]

    def add_iatacode_to_sheet(self, url, sheety):
        """Update each row in Sheety with a resolved IATA code."""
        last_response = None

        for city_info in sheety:
            new_url = f"{url}/{city_info['id']}"
            flight_codes = {
                "sheet1": {
                    "iataCode": city_info['iataCode'],
                }
            }
            # Example payload sent to Sheety:
            # {"sheet1": {"iataCode": "PAR"}}
            last_response = requests.put(url=new_url, json=flight_codes)
            last_response.raise_for_status()

        return last_response


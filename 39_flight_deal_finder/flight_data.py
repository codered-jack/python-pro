from dataclasses import dataclass


@dataclass
class FlightData:
    """Structured object used across the app to pass one flight deal."""

    # Example:
    # FlightData(
    #     price=89,
    #     departure_city_name="London",
    #     departure_airport_iata_code="LON",
    #     arrival_city_name="Paris",
    #     arrival_airport_iata_code="PAR",
    #     outbound_date="2026-03-03",
    #     inbound_date="2026-03-10",
    # )
    price: int
    departure_city_name: str
    departure_airport_iata_code: str
    arrival_city_name: str
    arrival_airport_iata_code: str
    outbound_date: str
    inbound_date: str


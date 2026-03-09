from dataclasses import dataclass
from typing import Optional


@dataclass
class FlightData:
    """Structured object for one flight deal returned by Tequila."""

    # Example:
    # FlightData(
    #     price=119,
    #     departure_city_name="London",
    #     departure_airport_iata_code="LON",
    #     arrival_city_name="Berlin",
    #     arrival_airport_iata_code="BER",
    #     outbound_date="2026-03-04",
    #     inbound_date="2026-03-11",
    #     via_city="Amsterdam",
    # )
    price: int
    departure_city_name: str
    departure_airport_iata_code: str
    arrival_city_name: str
    arrival_airport_iata_code: str
    outbound_date: str
    inbound_date: str
    via_city: Optional[str] = None


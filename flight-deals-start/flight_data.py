class FlightData:
    """
    A class used to hold details of flight deals.

    ...

    Attributes
    ----------
    price: int
        the price of the flight
    departure_city: str
        name of the departure city
    departure_airport_iata_code: str
        iata_code of departure airport
    arrival_city: str
        name of the arrival city
    arrival_city_iata_code: str
        iata_code of the arrival city
    outbound_date: date
        date of the departure flight
    inbound_date: date
        date of the inbound flight
    stop_overs: int, optional
        number of stop overs in the flight
    via_city: str, optional
        name of the stop over city

    """
    def __init__(self, price, departure_city, departure_airport_iata_code,
                 arrival_city, arrival_city_iata_code, outbound_date, inbound_date,
                 stop_overs=0, via_city=''):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport_iata_code = departure_airport_iata_code
        self.arrival_city = arrival_city
        self.arrival_city_iata_code = arrival_city_iata_code
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.stop_overs=stop_overs
        self.via_city=via_city
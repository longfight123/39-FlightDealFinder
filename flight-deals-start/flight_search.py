import requests
import datetime as dt
from flight_data import FlightData
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv('.env')
FLIGHT_SEARCH_API_KEY = os.getenv('FLIGHT_SEARCH_API_KEY')
FLIGHT_SEARCH_GET_URL = 'https://tequila-api.kiwi.com/v2/search'
FLIGHT_LOCATION_GET_URL = 'https://tequila-api.kiwi.com/locations/query'
FLY_FROM = 'YYC'
DEPARTURE_FROM_DATE = dt.datetime.now().strftime('%d/%m/%Y')
DEPARTURE_DATE_TIMEDELTA = dt.timedelta(days=180)
DEPARTURE_TO_DATE = (dt.datetime.now() + DEPARTURE_DATE_TIMEDELTA).strftime('%d/%m/%Y')

class FlightSearch:
    """
    A class used to search for flights.

    ...

    Attributes
    ----------
    get_request_data: None
        the data received from tequila's API
    headers: dictionary
        the tequila's API header

    Methods
    -------
    get_flight_data(city)
        searches for flight data to provided city and
        returns the information in a FlightData object
    get_flight_data_one_stopover(city)
        searches for flight data with one stopover to provided city
        and returns the information in a FlightData object
    """

    def __init__(self):
        self.get_request_data = None
        self.headers = {
            'apikey': FLIGHT_SEARCH_API_KEY
        }

    def get_flight_data(self, city):
        """searches for flight data to provided city and
        returns the information in a FlightData object

        Parameters
        ----------
        city: str
            The city you want to fly to
        """
        my_params = {
            'fly_from': FLY_FROM,
            'fly_to': city,
            'date_from': DEPARTURE_FROM_DATE,
            'date_to': DEPARTURE_TO_DATE,
            'adults': 1,
            'flight_type': 'round',
            'curr': 'CAD',
            'max_stopovers': 0,
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28
        }
        get_response = requests.get(url=FLIGHT_SEARCH_GET_URL, params=my_params, headers=self.headers)
        get_response.raise_for_status()
        self.get_request_data = get_response.json()
        try:
            data = self.get_request_data['data'][0]
        except IndexError:
            print(f'No direct flights to {city} currently. Trying to look for flights with one stop over.')
            flight_data_with_one_stopover = self.get_flight_data_one_stopover(city=city)
            return flight_data_with_one_stopover
        price = data['price']
        departure_city = data['route'][0]['cityFrom']
        departure_airport_iata_code = data['route'][0]['flyFrom']
        arrival_city = data['route'][0]['cityTo']
        arrival_city_iata_code = data['route'][0]['flyTo']
        outbound_date = data['route'][0]['local_departure'].split('T')[0]
        inbound_date = data['route'][1]['local_departure'].split('T')[0]
        return FlightData(price=price, departure_city=departure_city, departure_airport_iata_code=departure_airport_iata_code,
                          arrival_city=arrival_city, arrival_city_iata_code=arrival_city_iata_code, outbound_date=outbound_date,
                          inbound_date=inbound_date)

    def get_flight_data_one_stopover(self, city):
        """searches for flight data with one stopover to provided city
        and returns the information in a FlightData object

        Parameters
        ----------
        city: str
            the city you want to fly to
        """
        my_params = {
            'fly_from': FLY_FROM,
            'fly_to': city,
            'date_from': DEPARTURE_FROM_DATE,
            'date_to': DEPARTURE_TO_DATE,
            'adults': 1,
            'flight_type': 'round',
            'curr': 'CAD',
            'max_stopovers': 1,
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28
        }
        response = requests.get(url=FLIGHT_SEARCH_GET_URL, params=my_params, headers=self.headers)
        response.raise_for_status()
        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f'No flights with one stop over to {city} currently.')
            return None
        price = data['price']
        if len(data['route']) == 4:
            departure_city = data['route'][0]['cityFrom']
            departure_airport_iata_code = data['route'][0]['flyFrom']
            arrival_city = data['route'][1]['cityTo']
            arrival_city_iata_code = data['route'][1]['flyTo']
            outbound_date = data['route'][0]['local_departure'].split('T')[0]
            inbound_date = data['route'][3]['local_departure'].split('T')[0]
            stop_overs = 1
            via_city = data['route'][0]['cityTo']
        elif len(data['route']) == 3 and city == data['route'][0]['cityCodeTo']:
            departure_city = data['route'][0]['cityFrom']
            departure_airport_iata_code = data['route'][0]['flyFrom']
            arrival_city = data['route'][0]['cityTo']
            arrival_city_iata_code = data['route'][0]['flyTo']
            outbound_date = data['route'][0]['local_departure'].split('T')[0]
            inbound_date = data['route'][2]['local_departure'].split('T')[0]
            stop_overs = 1
            via_city = data['route'][1]['cityTo']
        elif len(data['route']) == 3 and city == data['route'][1]['cityCodeTo']:
            departure_city = data['route'][0]['cityFrom']
            departure_airport_iata_code = data['route'][0]['flyFrom']
            arrival_city = data['route'][1]['cityTo']
            arrival_city_iata_code = data['route'][1]['flyTo']
            outbound_date = data['route'][0]['local_departure'].split('T')[0]
            inbound_date = data['route'][2]['local_departure'].split('T')[0]
            stop_overs = 1
            via_city = data['route'][0]['cityTo']
        return FlightData(price=price, departure_city=departure_city,
                          departure_airport_iata_code=departure_airport_iata_code,
                          arrival_city=arrival_city, arrival_city_iata_code=arrival_city_iata_code,
                          outbound_date=outbound_date,
                          inbound_date=inbound_date, stop_overs=stop_overs, via_city=via_city)
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv('.env')
SHEETY_GET_API = os.getenv('SHEETY_GET_API')
SHEETY_PUT_API = os.getenv('SHEETY_PUT_API')
FLIGHT_LOCATION_GET_URL = 'https://tequila-api.kiwi.com/locations/query'
FLIGHT_SEARCH_API_KEY = os.getenv('FLIGHT_SEARCH_API_KEY')
FLIGHT_SEARCH_HEADERS = {
    'apikey': FLIGHT_SEARCH_API_KEY
}

class DataManager:
    """
    A class used to manage the google spreadsheet,
    obtain the lowest acceptable price from the
    google spreadsheet, and obtain the destination
    wish list from the google spreadsheet,
    and update IATA codes used in Tequila API.

    ...

    Attributes
    ----------
    get_request_data: None
        data holding the information from the spreadsheet

    Methods
    -------
    get_data()
        obtain the information from the spreadsheet
    find_iata_data()
        obtains the  IATA codes for each city
        in the spreadsheet
    put_iata_data()
        updates the spreadsheet with IATA codes
    """
    def __init__(self):
        self.get_request_data = None

    def get_data(self):
        """obtain the information from the spreadsheet
        """
        # make a get response and then store the data in self.get_request_data
        get_response = requests.get(url=SHEETY_GET_API)
        get_response.raise_for_status()
        self.get_request_data = get_response.json()

    def find_iata_data(self):
        """obtains the  IATA codes for each city
        in the spreadsheet
        """
        # Checks if the IATA Codes are empty, if they are, make a GET request to Tequila to obtain IATA codes
        if self.get_request_data['prices'][0]['iataCode'] == '':
            for row_in_copy_of_flight_deals in self.get_request_data['prices']:
                my_params = {
                    'term': row_in_copy_of_flight_deals['city'],
                    'location_types': 'city'
                }
                get_location_response = requests.get(url=FLIGHT_LOCATION_GET_URL, params=my_params, headers=FLIGHT_SEARCH_HEADERS)
                get_location_response.raise_for_status()
                location_data = get_location_response.json()
                iata_code = location_data['locations'][0]['code']
                row_in_copy_of_flight_deals['iataCode'] = iata_code

    def put_iata_data(self):
        """updates the spreadsheet with IATA codes
        """
        #Takes in an updated sheet_data with IATA codes inserted from FlightSearch and updates the Google Sheet
        for row in self.get_request_data['prices']:
            edited_record = {
                'price': {
                    'city': row['city'],
                    'iataCode': row['iataCode'],
                    'lowestPrice': row['lowestPrice']
                }
            }
            put_response = requests.put(url=f'{SHEETY_PUT_API}{row["id"]}', json=edited_record)
            put_response.raise_for_status()



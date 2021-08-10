"""

This script utilizes the 'Twilio', 'Sheety', 'Tequila' APIs
to create a flight deal finder and notification app.

This script requires that 'requests', 'twilio',
 'smtplib', and python_dotenv be installed within the Python
environment you are running this script in.

"""

from data_manager import DataManager
import requests
from pprint import pprint
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Make DataManager Class and import the get request response data into main.py
data_manager = DataManager()
data_manager.get_data()
data_manager.find_iata_data()
data_manager.put_iata_data()
# Make a loop so that if sheet_data IATA codes are empty, pass the city name to the FlightSearch class,
# it should use the API to return the iata code of that city and add it to the sheet_data
flight_search = FlightSearch()



#Here we get flight data for each of the cities in the google sheet from a city we specify -> to that city
#Then it checks the price of that flight against the lowest price we have in the Google Sheet, if the price is lower,
#Sends us a text notifcation
for row in data_manager.get_request_data['prices']:
    flight_data = flight_search.get_flight_data(row['iataCode'])
    try:
        if flight_data.price <= row['lowestPrice']:
            notification_manager = NotificationManager()
            notification_manager.send_sms(flight_data)
            notification_manager.send_emails(flight_data)
        else:
            print(f'The price is too high for {row["city"]}: {flight_data.price} > {row["lowestPrice"]}')
    except AttributeError:
        continue



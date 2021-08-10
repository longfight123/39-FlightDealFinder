from twilio.rest import Client
from flight_data import FlightData
import smtplib
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
USERS_SHEET_GET_ENDPOINT = os.getenv('USERS_SHEET_GET_ENDPOINT')
TWILIO_ID = os.getenv('TWILIO_ID')
TWILIO_APIKEY = os.getenv('TWILIO_APIKEY')


class NotificationManager:
    """
    A class used to send notifications
    when a suitable flight deal is found.

    ...

    Attributes
    ----------
    id: str
        the Twilio API id
    api_key: str
        the Twilio API key

    Methods
    -------
    send_sms(flight_data)
        sends an sms message with flight deal details
    send_emails(city)
        obtains a list of emails to notify of a flight deal
        and sends email notifications
    """
    def __init__(self):
        self.id = TWILIO_ID
        self.api_key = TWILIO_APIKEY

    def send_sms(self, flight_data: FlightData):
        """sends an sms message with flight deal details

        Parameters
        ----------
        flight_data: FlightData
            the object containing details of the flight deal
        """
        # client = Client(self.id, self.api_key)
        # message = client.messages \
        #     .create(
        #     body=f"\nLow Price Alert! Only ${flight_data.price} to fly from {flight_data.departure_city}"
        #          f"-{flight_data.departure_airport_iata_code} to {flight_data.arrival_city}"
        #          f"-{flight_data.arrival_city_iata_code}, from {flight_data.outbound_date} to {flight_data.inbound_date}.",
        #     from_='+12158678688',
        #     to='+14036693979'
        # )
        # print(message.status)

        print(f"\nLow Price Alert! Only ${flight_data.price} to fly from {flight_data.departure_city}"
                 f"-{flight_data.departure_airport_iata_code} to {flight_data.arrival_city}"
                 f"-{flight_data.arrival_city_iata_code}, from {flight_data.outbound_date} to {flight_data.inbound_date}. "
              f"{flight_data.stop_overs} stopovers via {flight_data.via_city}. ")

    def send_emails(self, flight_data: FlightData):
        """obtains a list of emails to notify of a flight deal
        and sends email notifications

        Parameters
        ----------
        flight_data: FlightData
            the object containing details of the flight deal
        """
        response = requests.get(url=USERS_SHEET_GET_ENDPOINT)
        response.raise_for_status()
        data = response.json()['users']
        email_list = []
        for row in data:
            email_list.append(row['email'])
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=GMAIL_USERNAME, password=GMAIL_PASSWORD)
            for email in email_list:
                connection.sendmail(from_addr=GMAIL_USERNAME, to_addrs=email,
                                    msg=f'Subject: Low Price Alert!\n\n Only ${flight_data.price} to fly from '
                                        f'{flight_data.departure_city}-{flight_data.departure_airport_iata_code} to'
                                        f' {flight_data.arrival_city}-{flight_data.arrival_city_iata_code}, from '
                                        f'{flight_data.outbound_date} to {flight_data.inbound_date}. {flight_data.stop_overs}'
                                        f' stopovers via {flight_data.via_city}.'
                                        f'\n https://www.google.co.uk/flights?hl=en#flt={flight_data.departure_airport_iata_code}'
                                        f'.{flight_data.arrival_city_iata_code}{flight_data.outbound_date}*{flight_data.arrival_city_iata_code}'
                                        f'.{flight_data.departure_airport_iata_code}.{flight_data.inbound_date}')

import requests
from dotenv import load_dotenv
import os
#  from .api_key import API_KEY
load_dotenv()

GOOGLE_KEY = os.getenv("google")


class GEOCODE:
    ''' Retrieve geocode for a given address '''
    def __init__(self, search):
        self.search = search
        #  self.URL = f'https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&api_key={API_KEY.get("nasa")}'  # noqa: E501
        #  was previously using this class method I wrote to load API keys from yaml, removed in favour of using dotenv instead  # noqa: E501
        self.URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={GOOGLE_KEY}'  # noqa: E501
        self.response = requests.get(self.URL)

    def loc(self):
        ''' Extract longitude/latitude from geocode information '''
        lon = self.response.json()['results'][0]['geometry']['location']['lng']
        lat = self.response.json()['results'][0]['geometry']['location']['lat']
        return(lon, lat)

    def check(self):
        ''' Check for requests response code '''
        return self.response

    def address(self):
        ''' Extract formatted address '''
        return self.response.json()['results'][0]['formatted_address']

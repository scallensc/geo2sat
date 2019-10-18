import requests
from dotenv import load_dotenv
import os
load_dotenv()

NASA_KEY = os.getenv("nasa")


class SATELLITE:
    ''' Request satellite image object from NASA API '''
    def __init__(self, lon, lat):
        ''' Initialise satellite object '''
        self.URL = f'https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&api_key={NASA_KEY}'  # noqa: E501
        self.response = requests.get(self.URL)

    def pic(self):
        ''' Extract image URL from satellite object '''
        image = self.response.json()['url']
        return image

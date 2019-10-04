import requests
from api_key import API_KEY

class GEOCODE:
    ''' Retrieve geocode for a given address '''
    def __init__(self, search):
        self.search = search
        self.URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={API_KEY.get("google")}'
        self.response = requests.get(self.URL)

    def loc(self, search):
        ''' Extract longitude/latitude from geocode information '''
        lon = self.response.json()['results'][0]['geometry']['location']['lng']
        lat = self.response.json()['results'][0]['geometry']['location']['lat']
        return(lon, lat)

    def check(self, search):
        ''' Check for 200 OK '''
        return self.response
    
    def address(self, search):
        ''' Extract formatted address '''
        return self.response.json()['results'][0]['formatted_address']
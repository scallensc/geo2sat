import yaml
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

class API_KEY:
    ''' Retrieve API keys from file '''
    def get(self):
        ''' Load API keys or display error if file not found'''
        APIKEYS = 'apikeys.yaml'
        try:
            with open(APIKEYS, 'r') as config_file:
                config = yaml.load(config_file)
                return config['apikeys'][self]
        except FileNotFoundError:
            print("'%s' file not found" % self)

google_key = API_KEY.get('google')
nasa_key = API_KEY.get('nasa')

class GEOCODE:
    ''' Retrieve geocode for a given address '''
    def get(self, search, google_key):
        ''' Retreieve longitude/latitude from geocode information '''
        URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={google_key}'
        lon = requests.get(URL).json()['results'][0]['geometry']['location']['lng']
        lat = requests.get(URL).json()['results'][0]['geometry']['location']['lat']
        return(lon, lat)

class SATELLITE:
    ''' Retrieve satellite imagery '''
    def get(self, lon, lat, nasa_key):
        ''' Request image based on longitude/latitude supplied by Geocode API '''
        URL = f'https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&api_key={nasa_key}'
        image = requests.get(URL).json()['url']
        return image

'''
TESTS
search = input('Please enter an address: ')
lon, lat = GEOCODE.get(None, search, google_key)
print(lon, lat)
image = SATELLITE.get(None, lon, lat, nasa_key)
print(image)
'''

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    query = request.form['text']
    lon, lat = GEOCODE.get(None, query, google_key)
    image = SATELLITE.get(None, lon, lat, nasa_key)
    return '<img src=' + image + '>'

if __name__ == '__main__':
    app.run()
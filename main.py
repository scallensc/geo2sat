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
    def check(self, search, google_key):
        ''' Check for 200 OK '''
        URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={google_key}'
        check = requests.get(URL)
        return check

class SATELLITE:
    ''' Retrieve satellite imagery '''
    def get(self, lon, lat, nasa_key):
        ''' Request image based on longitude/latitude supplied by Geocode API '''
        URL = f'https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&api_key={nasa_key}'
        image = requests.get(URL).json()['url']
        return image

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    ''' Get address from HTML form '''
    message = ''
    query = request.form['text']

    # check for active internet connection
    if query:
        try:
            GEOCODE.check(None, query, google_key)
        except requests.ConnectionError:
            message = "No internet connection!"
            return render_template('index.html', message=message)

    check = GEOCODE.check(None, query, google_key)
    # check for a valid 200 OK return code
    if check.status_code == 200:
        try:
            lon, lat = GEOCODE.get(None, query, google_key)
        except IndexError:
            # index error only appears to be raised if an invalid address
            # which cannot be found has been entered
            message = 'Invalid input, please try again!'
            return render_template('index.html', message=message)
        # return satellite image with formatted address for display on html page
        image = SATELLITE.get(None, lon, lat, nasa_key)
        message = GEOCODE.check(None, query, google_key).json()['results'][0]['formatted_address']
        return render_template('index.html', image=image, message=message)
    else:
        # return error message for a blank input
        message = 'Nothing Entered, please try again!'
        return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

'''
TESTS
search = input('Please enter an address: ')
lon, lat = GEOCODE.get(None, search, google_key)
print(lon, lat)
image = SATELLITE.get(None, lon, lat, nasa_key)
print(image)
'''

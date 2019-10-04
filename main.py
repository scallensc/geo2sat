import requests
from flask import Flask, render_template, request
import yaml

app = Flask(__name__)
class API_KEY:
    ''' Retrieve API keys from file '''
    def get(self):
        ''' Load API keys or display error if file not found '''
        try:
            with open('apikeys.yaml', 'r') as config_file:
                config = yaml.load(config_file)
                return config['apikeys'][self]
        except FileNotFoundError:
            print("'%s' file not found" % self)

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

class SATELLITE:
    ''' Request satellite image object from NASA API '''
    def __init__(self, lon, lat):
        ''' Initialise satellite object '''
        self.URL = f'https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&api_key={API_KEY.get("nasa")}'
        self.response = requests.get(self.URL)
    
    def pic(self):
        ''' Extract image URL from satellite object '''
        image = self.response.json()['url']
        return image

@app.route('/')
def form():
    ''' Load index page from template '''
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    ''' Get address from HTML form '''
    message = ''
    query = request.form['text']
    geocode = GEOCODE(query)
    # check for active internet connection
    if query:
        try:
            geocode.check(query)
        except requests.ConnectionError:
            message = "No internet connection!"
            return render_template('index.html', message=message)

    # check for a valid 200 OK return code
    if geocode.check(query).status_code == 200:
        try:
            lon, lat = geocode.loc(query)
        except IndexError:
            # index error only appears to be raised if an invalid address
            # which cannot be found has been entered
            message = 'Invalid input, please try again!'
            return render_template('index.html', message=message)
        
        # retrieve formatted address to display as message
        # along with satellite image to render on html page
        message = geocode.address(query)
        image = SATELLITE(lon, lat).pic()

        return render_template('index.html', image=image, message=message)

    # return error message for a blank input
    message = 'Nothing Entered, please try again!'
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)


import requests
from flask import Flask, render_template, request
from geocode import GEOCODE
from satellite import SATELLITE
from api_key import API_KEY
import yaml

app = Flask(__name__)

@app.route('/')
def form():
    ''' Load index page from template '''
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    ''' Get address from HTML form '''
    message = ''
    query = request.form['text']
    
    # check for active internet connection
    try:
        geocode = GEOCODE(query)
    except requests.ConnectionError:
            message = "No internet connection!"
            return render_template('index.html', message=message)

    # check for a valid 200 OK return code
    if geocode.check().status_code == 200:
        try:
            lon, lat = geocode.loc()
        except IndexError:
            # index error only appears to be raised if an invalid address
            # which cannot be found has been entered
            message = 'Invalid input, please try again!'
            return render_template('index.html', message=message)
        
        # retrieve formatted address to display as message
        message = geocode.address()
        
        # check for active internet connection for second API call
        try:
            image = SATELLITE(lon, lat).pic()
        except requests.ConnectionError:
            message = "No internet connection!"
            return render_template('index.html', message=message)

        return render_template('index.html', image=image, message=message)

    # return error message for a blank input
    message = 'Nothing Entered, please try again!'
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)


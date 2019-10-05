import requests
from flask import Flask, render_template, request
from geocode import GEOCODE
from satellite import SATELLITE


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

    # Check for active internet connection
    try:
        geocode = GEOCODE(query)
    except requests.ConnectionError:
        message = "No internet connection!"
        return render_template('index.html', message=message)

    # Check for a valid 200 OK return code
    if geocode.check().status_code == 200:
        try:
            lon, lat = geocode.loc()
        except IndexError:
            # Index error only appears to be raised if an invalid address
            # which cannot be found has been entered
            message = 'Invalid input, please try again!'
            return render_template('index.html', message=message)

        # Retrieve formatted address to display as message
        message = geocode.address()

        # Check for any exceptions for second API call
        # program will not reach this call unless the first
        # API returned successfully, as such any error raised
        # here is due to an issue with the NASA API itself
        try:
            image = SATELLITE(lon, lat).pic()
        except Exception:
            message = "Error communicating with NASA API, please try again!"
            return render_template('index.html', message=message)

        return render_template('index.html', image=image, message=message)

    # Return error message for a blank input
    message = 'Nothing Entered, please try again!'
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

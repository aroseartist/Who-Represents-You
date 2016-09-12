"""Server file for Hb project."""

# Import necessary modules, etc.
# Access google maps API: exchange city,state for lat,lng
import geocoder
import geojson
import googlemaps
# Utilize Jinja for HTML templates
import Jinja2
import json
# Access local env variables
import os
import sys
# Access sunlight API for Leg & Words data
import sunlight
import sunlight.service

# Utilize Flask libraries
from flask import (Flask, render_template, redirect, request, flash, jsonify)
# Use toolbar for debugging
# from flask_debugtoolbar import DebugToolbarExtension
from Jinja2 import StrictUndefined
# Access JSON
from pprint import pprint
from sunlight import (congress, capitolwords)
from sunlight.service import EntityDict, EntityList
from sys import argv

app = Flask(__name__, static_url_path='/static')
# Required to use Flask sessions and debug toolbar
app.secret_key = 'FLASK_SECRET_KEY'
# Access key for Sunlight API
sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
# Access key for Googlemaps API
gmaps = googlemaps.Client(key=os.environ['GEOLOCATE_GOOGLE_API'])

# Ensures undefined variables in jinja raise an error
app.jinja_env.undefined = StrictUndefined
# allows html to reload without restarting server
app.jinja_env.auto_reload = True


###################### Core Routes ###########################

@app.route('/')
# Routes app index page to homepage
def index():
    """Homepage."""
    return render_template("home.html", city=None)

@app.route('/statejson')
# Routes state coordinates to svg file for D3 map rendering
def state_json_root():
    return app.send_static_file('us-states.json')


##################### API Calls ###############################

@app.route('/repdetails', methods=['POST'])
# Routes details from sunlight Legs api to jinja template

def gather_sunlight_congress():
    """Return lat,lng based on city, state and then

    Find members of Congress from Sunlight via lat lng.
    """

    # Get form variables from home.html user input
    city = request.form["city"]
    state = request.form["state"]
    # Concatinate city, state to send to Googlemaps API / Geocoder
    location = city + ", " + state

    # Convert city, state to lat, lng via Geocoder
    g = geocoder.google(location)
    latlng = g.latlng

    # Send lat, lng to Sunlight, requesting leg details
    # Returns as JSON EntityList
    leg_details_congress = sunlight.congress.locate_legislators_by_lat_lon(latlng[0], 
                                                                            latlng[1])
    leg_details_openstates = sunlight.openstates.legislator_geo_search(latlng[0], 
                                                                        latlng[1])

    # Pass returned JSON details to Jinja
    return render_template("home.html",
                            leg_details_congress=leg_details_congress,
                            leg_details_openstates=leg_details_openstates,
                            state=state,
                            city=city)


################### jQuery / AJAX Calls #####################

@app.route('/getstatewords.json')
def get_state_words():
    """Return most used words by legislators of clicked state."""

    # Accept argument data from D3 map .onclick function
    clickedstate = request.args.get('state')

    # Get form variables from home.html user input
    # Send query to sunlight requesting words data
    topwords_per_state = sunlight.capitolwords.phrases(entity_type='state', 
                                                        entity_value=clickedstate, 
                                                        per_page=10)
    state_words_plus_count = []

    for count_dict in topwords_per_state:
        # Make a tuple to pass back to state words container
        count = count_dict['count']
        word = count_dict['ngram']

        count_word = (count, word)
        state_words_plus_count.append(count_word)

    # Put words in descending order by frequency
    state_words_plus_count.reverse()

    # Jsonify list of tuples for use and pass back to container
    return jsonify({'topwords':state_words_plus_count})


@app.route('/getlegwords.json')
def get_leg_words():
    """Return most used words by a particular legislator."""

    # Accept argument data from legislator event listener function
    clickedleg = request.args.get('bioguide_id')

    # Get form variables from home.html user input
    # Send query to sunlight requesting words data
    topwords_per_leg = sunlight.capitolwords.phrases(entity_type='legislator', 
                                                        entity_value=clickedleg)
    legs_words = []

    for count_dict in topwords_per_leg:
        # Make a tuple to pass back to legislator words container
        size = count_dict['count']
        text = count_dict['ngram']
        size_text = (size, text)
        legs_words.append(size_text)

    # Put words in order by frequency
    legs_words.sort()
    # Sort descending
    legs_words.reverse()
    # Jsonify list of tuples for use and pass back to container
    return jsonify({'legwords':legs_words})


################### Helper Functions #######################

# Listening or requests
if __name__ == "__main__":

    
    # Set debug=True in order to invoke the DebugToolbarExtension
    # app.debug = True

    # app.config['TRAP_HTTP_EXCEPTIONS'] = True
    
    # Use of debug toolbar
    # DebugToolbarExtension(app)
   
    # connect_to_db(app)

    # Run app locally
    # app.run(host='0.0.0.0')
    
    #  Run app via Heroku
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)


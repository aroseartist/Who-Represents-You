""" Server file for Hb project """
# Import necessary modules, etc.

# Access local env variables
import os
import sys
from sys import argv
import json

# Utilize Jinja for HTML templates
import Jinja2
from Jinja2 import StrictUndefined

# Access sunlight API for Leg & Words data
import sunlight
from sunlight import (congress, capitolwords)
import sunlight.service
from sunlight.service import EntityDict, EntityList

# Access google maps API: exchange city,state for lat,lng
import geocoder
import googlemaps
import geojson

# from model import (topwords_per_state_JSON2List, usword_usedwhere_JSON2List)

# Connect to model.py to access databases
# from model import Legislators, connect_to_db, db

# Utilize Flask and its libraries
from flask import (Flask, render_template, redirect, request, flash, jsonify)
# Use toolbar for debugging
# from flask_debugtoolbar import DebugToolbarExtension
# Access JSON
from pprint import pprint

app = Flask(__name__, static_url_path='/static')

# Required to use Flask sessions and debug toolbar
app.secret_key = "tHiSiSmyWiTTlEseCrEt"
# Ensures undefined variables in jinja raise an error
app.jinja_env.undefined = StrictUndefined
# allows html to reload without restarting server
app.jinja_env.auto_reload = True


###################### Core Routes ###########################

@app.route('/')
# Routes app index page to homepage
def index():
    """ Homepage """
    return render_template("home.html", city=None)

@app.route('/statejson')
# Routes state coordinates to svg file for D3 map rendering
def statejsonroot():
    return app.send_static_file('us-states.json')


##################### API Calls ###############################

@app.route('/repdetails', methods=['POST'])
# Routes details from sunlight Legs api to jinja template

def gather_sunlight_congress():
    """
    Return lat,lng based on city, state and then

    Find members of Congress from Sunlight via lat lng
    """
    # Access key for Googlemaps API
    gmaps = googlemaps.Client(key=os.environ['GEOLOCATE_GOOGLE_API'])
    # Access key for Sunlight API
    sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'

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
    leg_details_congress = sunlight.congress.locate_legislators_by_lat_lon(latlng[0], latlng[1])
    leg_details_openstates = sunlight.openstates.legislator_geo_search(latlng[0], latlng[1])

    # Pass returned JSON details to Jinja
    return render_template("home.html",
                            leg_details_congress=leg_details_congress,
                            leg_details_openstates=leg_details_openstates,
                            state=state,
                            city=city)


##################### jQuery / AJAX Calls #############################

@app.route('/getstatewords.json')
def getstatewords():
    """
    Return most used words by legislators of clicked state
    """

    # Accept argument data from D3 map .onclick function
    clickedstate = request.args.get('state')

    # Access key for Sunlight API
    sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
    
    # Get form variables from home.html user input
    # Send query to sunlight requesting words data
    topwords_per_state = sunlight.capitolwords.phrases(entity_type='state', entity_value=clickedstate, per_page=10)
    list_of_tuples = []

    for count_dict in topwords_per_state:
        # Make a tuple to pass back to state words container
        count = count_dict['count']
        # if ngram != "...":
        word = count_dict['ngram']
        # else:
        cw_tuple = (count, word)
        list_of_tuples.append(cw_tuple)

    # Put words in descending order by frequency
    list_of_tuples.reverse()

    # Jsonify list of tuples for use and pass back to container
    return jsonify({'topwords':list_of_tuples})


@app.route('/getlegwords.json')
def getlegwords():
    """
    Return most used words by a particular legislator
    """

    # Accept argument data from legislator event listener function
    clickedleg = request.args.get('bioguide_id')
    # Access key for Sunlight API
    sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
    
    # Get form variables from home.html user input
    # Send query to sunlight requesting words data
    topwords_per_leg = sunlight.capitolwords.phrases(entity_type='legislator', entity_value=clickedleg)
    tuple_of_words = []

    for count_dict in topwords_per_leg:
        # Make a tuple to pass back to legislator words container
        size = count_dict['count']
        text = count_dict['ngram']
        st_tuple = (size, text)
        tuple_of_words.append(st_tuple)

    # Put words in order by frequency
    tuple_of_words.sort()
    # Sort descending
    tuple_of_words.reverse()
    # Jsonify list of tuples for use and pass back to container
    return jsonify({'legwords':tuple_of_words})


################### Helper Functions ##########################

# Listening or requests
if __name__ == "__main__":

    
    # Set debug=True in order to invoke the DebugToolbarExtension
    # app.debug = True

    # app.config['TRAP_HTTP_EXCEPTIONS'] = True
    
    # Use of debug toolbar
    # DebugToolbarExtension(app)
   
    # connect_to_db(app)

    # Run app locally
    app.run(host='0.0.0.0')


""" Server file for Hb project """
# import necessary modules, etc.

# access local env variables
import os
import sys
from sys import argv
import csv
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

from model import (topwords_per_state_JSON2List, usword_usedwhere_JSON2List)

# Connect to model.py to access databases
# from model import Legislators, connect_to_db, db

# Utilize Flask and its libraries
from flask import (Flask, render_template, redirect, request, flash, jsonify)
# Use toolbar for debugging
from flask_debugtoolbar import DebugToolbarExtension
# Access JSON
from pprint import pprint

app = Flask(__name__, static_url_path='/static')
# Required to use Flask sessions and debug toolbar
app.secret_key = "tHiSiSmyWiTTlEseCrEt"
# Ensures undefined variables in jinja raise an error
app.jinja_env.undefined = StrictUndefined
# allows html to reload without restarting server
app.jinja_env.auto_reload = True

###################### Core routes ###########################

@app.route('/')
# Routes app index page to homepage
def index():
    """ Homepage """
    return render_template("home.html", city=None)

@app.route('/statejson')
# Routes state coordinates to svg file for D3 map rendering
def statejsonroot():
    return app.send_static_file('us-states.json')

##################### API calls ###############################

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

##################### AJAX calls #############################

@app.route('/getstatewords.json')
def getstatewords():
	clickedstate = request.args.get('state')

	# Access key for Sunlight API
	sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
	
	# Get form variables from home.html user input
	# Send query to sunlight requesting words data
	topwords_per_state = sunlight.capitolwords.phrases(entity_type='state', entity_value=clickedstate, per_page=15)
	list_of_tuples = []

	for count_dict in topwords_per_state:
		# make a tuple
		count = count_dict['count']
		word = count_dict['ngram']
		cw_tuple = (count, word)
		list_of_tuples.append(cw_tuple)

	list_of_tuples.reverse()

	return jsonify({'topwords':list_of_tuples})


@app.route('/getlegwords.json')
def getlegwords():
	clickedleg = request.args.get('bioguide_id')

	# Access key for Sunlight API
	sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
	
	# Get form variables from home.html user input
	# Send query to sunlight requesting words data
	topwords_per_leg = sunlight.capitolwords.phrases(entity_type='legislator', entity_value=clickedleg, per_page=15)
	
	list_of_tuples = []

	for count_dict in topwords_per_leg:
		# make a tuple
		count = count_dict['count']
		word = count_dict['ngram']
		cw_tuple = (count, word)
		list_of_tuples.append(cw_tuple)

	list_of_tuples.reverse()

	return jsonify({'topwords':list_of_tuples})


# @app.route('/topwords', methods=['POST'])
# # Routes details from sunlight api to jinja template
# def topwords_usedwhere():
# 	""" Return top federal words based on state frequency """

# 	# Access key for Sunlight API
# 	sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
	
# 	# Get form variables from home.html user input
# 	word = request.form["word"]
# 	# Send query to sunlight requesting words data
# 	us_topwords_usedwhere = sunlight.capitolwords.phrases_by_entity(entity_type='state', phrase=word, per_page=10)

# 	# Convert JSON into dictionary, then call next function
# 	# from model.py: topwords_per_state_JSON2List(topwords_per_state)
# 	us_topwords_usedwhere_list = real_usword_usedwhere_JSON2List(usword_usedwhere)
	
# # 	# return jsonify(data=state_words_list)
# 	# WORD_CSV = jsonify(usword_usedwhere_list)


# 	# federal_words_dict = {}
#  #    federal_words_list = []

#  #    for state_count in us_topwords_usedwhere:
#  #        # import pdb; pdb.set_trace()
#  #        federal_words_dict[int(state_count["count"])] = str(state_count["state"])

#  #    for key in state_words_dict:
#  #        mini_state_words = {}
#  #        key_count = federal_words_dict[key]
#  #        mini_federal_words[key] = key_count
#  #        federal_words_list.append(mini_state_words)
#  #        # instead of making mini_dict be {634: 'congress'}
#  #        # structure mini_dict like this:  {'state':'MO', 'count': 634}
        
#  #    # print state_words_dict
#  #    return usword_usedwhere_list


# 	# Convert JSON to csv file
# # with open('mycsvfile.csv','wb') as f:
# #     w = csv.writer(f)
# #     w.writerows(WORD_CSV.items())
#     # w = csv.writer(sys.stderr)

# 	# Pass returned details to Jinja
# 	return render_template("home.html/#topwords",
# 							us_topwords_usedwhere=us_topwords_usedwhere,
# 							word=word)



# @app.route('/statewords', methods=['POST'])
# # Routes details from sunlight api to jinja template
# def topwords_per_state():
# 	""" Returns the most used words per state """

# 	# Access key for Sunlight API
# 	sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY'
	
# 	# Get form variables from home.html user input
# 	state = request.form["state"]
# 	# Send query to sunlight requesting words data
# 	topwords_per_state = sunlight.capitolwords.phrases(entity_type='state', entity_value=state, per_page=10)

# 	# Convert JSON into dictionary, then call next function
# 	# from model.py: topwords_per_state_JSON2List(topwords_per_state)
# 	topwords_per_state_list = topwords_per_state_JSON2List(topwords_per_state)
	
# 	# # Convert JSON to csv file
# 	# with open('mycsvfile.csv','wb') as f:
# 	#     # w = csv.writer(sys.stderr)
# 	#     w = csv.writer(f)
# 	#     w.writerows(my_dict.items())

# 	# Pass returned details to Jinja
# 	return render_template("home.html/#statewords",
# 							topwords_per_state=topwords_per_state,
# 							state=state)


################### Helper functions ##########################

# Listening or requests
if __name__ == "__main__":
	
	# Set debug=True in order to invoke the DebugToolbarExtension
    app.debug = True

    # Use of debug toolbar
    DebugToolbarExtension(app)
   
    # connect_to_db(app)

    # Run app locally
    app.run(host='0.0.0.0')


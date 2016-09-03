# Who Represents You

## [Table of Contents](id:contents)

* [About](#about)
* [Technologies](#tech)
* [Run Locally](#run)
* [How to Use](#use)
* [Implementation](#implement)
* [Author](#author)
* [References](#ref)

***

## [About](#about)

Peek behind the curtain and get to know your represent]atives. Do their social media rants line up with their focus at the state level or on the hill? Assess their platform and hold them to their word by visualizing and considering the words they use each day while in session.

Check out the most popular words spoken by legislators of a chosen state, gaining insight into the way in which lawmakers shape and are shaped by their constituents. Users can search for contact information and social details of their federal, state, and local representatives.

***

## [Technologies](#tech)

**Dependencies:** [requirements.txt](https://github.com/aroseartist/Who-Represents-You/README.md "Dependencies")

[Python 2.7](https://www.python.org/ "Python")    | [Javascript](https://www.python.org/ "Javascript")    | **[Capitol Words API](http://sunlightlabs.github.io/Capitol-Words/ "Sunlight: Capitol Words")**
:----------- | :-----------: | -----------:
**[Flask](http://flask.pocoo.org/ "Flask")**           | **[jQuery](https://jquery.com/ "jQuery")**           | **[Sunlight: Congress API](https://sunlightlabs.github.io/congress/ "Sunlight: Congress")**
**[SQLAlchemy](http://www.sqlalchemy.org/ "SQLAlchemy")**           | **[Bootstrap](http://getbootstrap.com/ "Bootstrap")**           | **[Open States API](http://sunlightlabs.github.io/openstates-api/ "Sunlight: Open States")**
**[AJAX / JSON](https://api.jquery.com/category/ajax/ "AJAX")**           | **[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS "CSS")**           | **[Google Maps API](https://developers.google.com/maps/ "Google Maps")**
**[D3](https://d3js.org/ "D3")**           | **[Jinja2](http://jinja.pocoo.org/ "Jinja2")**           | **[Twitter API](https://dev.twitter.com/ "Twitter")**

***

## [Run Locally](#run)
###(Flask App)

Create a local directory to work within

	$ mkdir -p YOUR_DIRECTORY_NAME_HERE

Clone this repository and cd into it
	
	$ git clone https://github.com/aroseartist/Who-Represents-You YOUR_DIRECTORY_NAME_HERE
	
	$ cd ~/YOUR_DIRECTORY_NAME_HERE

Create your python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/ "VirtualEnv") and activate it

	$ virtualenv env
	
	$ source env/bin/activate

Install the required Python packages & dependencies
	
	$ pip install -r requirements.txt

Visit the [API](#api) locations and get a secret_key for each.

Create a secrets.sh file

	$ touch secrets.sh YOUR_DIRECTORY_NAME_HERE

Open and add (or simply CAT on the command line) your secret keys into secrets.sh

	export SUNLIGHT_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export GEOLOCATE_GOOGLE_API = "REPLACE_WITH_YOUR_KEY"  
	export GOOGLE_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export TWITTER_SECRET_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export TWITTER_SECRET_ACCESS_API_KEY = "REPLACE_WITH_YOUR_KEY"

Give your app access to this file

	$ source secrets.sh

In your command line, start up the flask server
	
	$ python server.py
	
In your borwser, go to localhost:5000 to see the web app

***

## [How to Use](#use)

### Popular Words by State Representatives

For each state, you can visualize the Congressional Record in relation to each states legislators. Click on a state and view their most frequently used words. This provides a quick overview of the issues being addressed by that states representatives on the Senate and House floors.

Who Represents You - Popular Words by Utah Representatives

![Capitol Words Map](https://github.com/aroseartist/Who-Represents-You/markdown/WRY.map.png "Map")

Enter a city and select a state: view image, party affiliation, and details about each local, state, and federal representative. Visit their website, call their office with a single click, check out to their social media accounts, and interact with their Twitter feed directly from this app.

Who Represents You - Representative Search

![Representative Search](https://github.com/aroseartist/Who-Represents-You/markdown/WRY.repfind.png "Representative Search")

Who Represents You - Representative Details

![Representative Details](https://github.com/aroseartist/Who-Represents-You/markdown/WRY.reps.png "Representative Details")



***

## [Implementation](#implement)

The front-end is composed of an SVG map whose paths are created with coordinates via JSON. Map interactivity is programmed with a combination of D3, Javascript, jQuery, and AJAX. Each evening, the Congressional Record is parsed and marked up by the [Sunlight Foundation](http://sunlightfoundation.com/ "Sunlight Foundation"). Their Capitol Words API provides access to the incoming data we see here.



***

## [Author](#author)

Lora "Ro" Rose is a software engineer from San Francisco, CA with a background in data and analytics program development. After obtaining a Master of Science in Marketing with a concentration in New Media, she has persued software engineering as a route to developing a career in data visualization. Visit her online:

[Personal Website](http://www.aroseartist.com/ "ARoseArtist")

[LinkedIn](linkedin.com/in/aroseartist "Lora Rose")

***

## [References](#ref)



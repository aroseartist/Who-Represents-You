# Who Represents You

## [Table of Contents](id:contents)

* [About](#about)
* [Run Locally](#run)
* [Technologies](#tech)
* [API Use](#api)
* [How to Use](#use)
* [Author](#author)
* [References](#ref)

***

## [About](#about)

Peek behind the curtain and get to know your represent]atives. Do their social media rants line up with their focus at the state level or on the hill? Assess their platform and hold them to their word by visualizing and considering the words they use each day while in session. Check out the most popular words spoken by legislators of a chosen state, gaining insight into the way in which lawmakers shape and are shaped by their constituents. Users can search for contact information and social details of their federal, state, and local representatives.

***

## [Run Locally](#run)
###(Flask App)

Create a local directory, clone the code repository and cd into it

	mkdir -p YOUR_DIRECTORY_NAME_HERE
	cd ~/dev

Clone this repository
	
	git clone https://github.com/aroseartist/Who-Represents-You YOUR_DIRECTORY_NAME_HERE

Create your python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/ "VirtualEnv") 

Install the required Python packages & dependencies
	
	pip install -r requirements.txt

Visit the [API](#api) locations and get a secret_key for each.

Create a secrets.sh file

	touch secrets.sh YOUR_DIRECTORY_NAME_HERE

Open and add (or simply CAT on the command line) your secret keys into secrets.sh like so

	export SUNLIGHT_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export GEOLOCATE_GOOGLE_API = "REPLACE_WITH_YOUR_KEY"  
	export GOOGLE_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export TWITTER_SECRET_API_KEY = "REPLACE_WITH_YOUR_KEY"  
	export TWITTER_SECRET_ACCESS_API_KEY = "REPLACE_WITH_YOUR_KEY"

Give your app access to this file

	source secrets.sh

In your command line, start up the flask server
	
	python server.py
	
In your borwser, go to localhost:5000 to see the web app

***

## [Technologies](#tech)

* [Javascript](https://www.python.org/ "Javascript")
* [Python 2.7](https://www.python.org/ "Python")
* [Flask](http://flask.pocoo.org/ "Flask")
* [Flask - SQLAlchemy](http://www.sqlalchemy.org/ "SQLAlchemy")
* [jQuery](https://jquery.com/ "jQuery")
* [AJAX / JSON](https://api.jquery.com/category/ajax/ "AJAX")
* [Jinja2](http://jinja.pocoo.org/ "Jinja2")
* [Bootstrap](http://getbootstrap.com/ "Bootstrap")
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS "CSS")
* [D3](https://d3js.org/ "D3")

**Dependencies:** [requirements.txt](https://github.com/aroseartist/Who-Represents-You/README.md "Dependencies")

***

## [API Use](#api)

* [Sunlight: Capitol Words](http://sunlightlabs.github.io/Capitol-Words/ "Sunlight: Capitol Words")
* [Sunlight: Congress](https://sunlightlabs.github.io/congress/ "Sunlight: Congress")
* [Sunlight: Open States](http://sunlightlabs.github.io/openstates-api/ "Sunlight: Open States")
* [Google Maps](https://developers.google.com/maps/ "Google Maps")
* [Twitter](https://dev.twitter.com/ "Twitter")

***

## [How to Use](#use)




***

## [Author](#author)

Lora "Ro" Rose is a software engineer from San Francisco, CA. Visit her online:

[Personal Website](http://www.aroseartist.com/ "ARoseArtist")

[LinkedIn](linkedin.com/in/aroseartist "Lora Rose")

***

## [References](#ref)



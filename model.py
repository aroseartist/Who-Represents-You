""" Models and database functions. """

# This is the connection to the PostgreSQL database
# We're getting this through the Flask-SQLAlchemy helper library.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from sunlight.errors import InvalidRequestException, BadRequestException
import sunlight.service
import json

service_url = "http://capitolwords.org/api/1"

################################################################
# Model definitions

def topwords_per_state_JSON2List(topwords_per_state):

    state_words_dict = {}
    state_words_list = []

    for k in topwords_per_state:
    # instead of making mini_dict be {634: 'congress'}
    # structure mini_dict like this:  {'state':'MO', 'count': 634}   
        state_words_dict[int(k["count"])] = str(k["ngram"])
        # print("{} = {}".format(key, d[key]))
        # key, counts[key]

    for key in state_words_dict:
        mini_state_words = {}

        key_count = state_words_dict[key]
        mini_state_words[key] = key_count

        state_words_list.append(mini_state_words)
        
    # print state_words_dict
    return state_words_list
    # >>> [{'opposition': 4093}]


def usword_usedwhere_JSON2List(usword_usedwhere):

    federal_words_dict = {}
    federal_words_list = []

    for state_count in usword_usedwhere:
        # import pdb; pdb.set_trace()
        federal_words_dict[str(state_count["state"])] = int(state_count["count"])

    for key in federal_words_dict:
        mini_federal_words = {}
        key_count = federal_words_dict[key]
        mini_federal_words[key] = key_count
        federal_words_list.append(mini_federal_words)
        # instead of making mini_dict be {634: 'congress'}
        # structure mini_dict like this:  {'state':'MO', 'count': 634}
        
    # print state_words_dict
    return federal_words_list




# class CapitolWords(sunlight.service.Service):
#     """ Access capitolwords API """

#     # Query phrase by entity_type and entity_value
#     def phrases(self, entity_type, entity_value, **kwargs):
#          """ Query top phrases for arguements """
            
#         # Arguments include date, month, state or legislator
#         kwargs['entity_type'] = entity_type
#         kwargs['entity_value'] = entity_value

#         return self.get(["phrases"], **kwargs)


#     # Query phrase by entity_type
#     def phrases_by_entity(self, legislator, **kwargs):
#         """ Query top facets for a given phrase.
        
#         For a list of arguments see `Capitol Words' phrases/entity.json
#         endpoint <http://capitolwords.org/api/#phrases/entity.json>`_.
#         """

#         # Arguments include date, month, state or legislator
#         return self.get(["phrases", entity_type], **kwargs)


################################################################
# API implementation methods

    # Gather JSON details from API and join for accessibility
    # def _get_url(self, pathparts, apikey, **kwargs):
    #     # Join pieces by slashes and add a trailing slash
    #     endpoint_path = "/".join(pathparts)

    #     #
    #     ret = "%s/%s.json?apikey=%s&%s" % (
    #         # Service url
    #         # http://capitolwords.org/api/1,
    #         # Endpoint path
    #         # http://capitolwords.org/api/1/dates.json?apikey='SUNLIGHT_API_KEY',
    #         # Sunlight API key access
    #         sunlight.config.KEY_ENVVAR = 'SUNLIGHT_API_KEY',
    #         # Sunlight encoding
    #         sunlight.service.safe_encode(kwargs)
    #     )
    #     return ret

    # # Decode returned JSON EntityList
    # def _decode_response(self, response):
    #     # Convert JSON
    #     ret = json.loads(response)
    #     # Error in output results in Invalid Request response
    #     if "error" in ret:
    #         ex = InvalidRequestException(ret['error'])
    #         ex.response = ret
    #         raise ex
    #     # Return results if no error
    #     if "results" in ret:
    #         return ret['results']
    #     # XXX: Verify this is actually what we want.
    #     return ret


################################################################
# Helper functions

def connect_to_db(app):
    """Connects database to Flask app"""

    # Configured for use of PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///legislators'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Allows for running of module interactively in order to work 
    # with and access the db directly

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()


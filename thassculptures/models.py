from endpoints_proto_datastore.ndb.model import EndpointsModel
from google.appengine.ext import ndb


class Sculpture(EndpointsModel):
    _message_fields_schema = ("entityKey", "title", "artist", "description", "image", "location")
    title = ndb.StringProperty();
    artist = ndb.StringProperty();
    description = ndb.StringProperty();
    image = ndb.StringProperty();
    location = ndb.StringProperty();

class Artist(EndpointsModel):
    _message_fields_schema = ("entityKey", "fname", "lname", "website_url", "description")
    fname = ndb.StringProperty();
    lname = ndb.StringProperty();
    website_url = ndb.StringProperty();
    description = ndb.StringProperty();

class Comment(EndpointsModel):
    _message_fields_schema = ("entityKey", "sculpture_key", "author", "content", "timestamp")
    sculpture_key = ndb.StringProperty();
    author = ndb.StringProperty();
    content = ndb.StringProperty();
    timestamp = ndb.DateTimeProperty(auto_now=True);
    
    
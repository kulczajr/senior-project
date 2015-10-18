from endpoints_proto_datastore.ndb.model import EndpointsModel
from google.appengine.ext import ndb


class Sculpture(EndpointsModel):
    _message_fields_schema = ("entityKey", "title", "artist", "description", "image", "audio", "location", "artist_key","do","think")
    title = ndb.StringProperty();
    artist = ndb.StringProperty();
    description = ndb.StringProperty();
    image = ndb.StringProperty();
    audio = ndb.BlobProperty();
    location = ndb.StringProperty();
    artist_key = ndb.StringProperty();
    do = ndb.StringProperty();
    think = ndb.StringProperty();

class Artist(EndpointsModel):
    _message_fields_schema = ("entityKey", "fname", "lname", "website_url", "description", "image")
    fname = ndb.StringProperty();
    lname = ndb.StringProperty();
    website_url = ndb.StringProperty();
    description = ndb.StringProperty();
    image = ndb.StringProperty();

class Comment(EndpointsModel):
    _message_fields_schema = ("entityKey", "sculpture_key", "author", "content", "timestamp", "is_approved")
    sculpture_key = ndb.StringProperty();
    author = ndb.StringProperty();
    content = ndb.StringProperty();
    timestamp = ndb.DateTimeProperty(auto_now=True);
    is_approved = ndb.BooleanProperty();
    
class Tour(EndpointsModel):
    _message_fields_schema = ("entityKey", "sculpture_list", "description")
    sculpture_list = ndb.StringProperty(repeated=True);
    description = ndb.StringProperty();    

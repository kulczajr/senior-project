from endpoints_proto_datastore.ndb.model import EndpointsModel
from google.appengine.ext import ndb


class Sculpture(EndpointsModel):
    title = ndb.StringProperty();
    artist = ndb.KeyProperty();
    description = ndb.StringProperty();
    image = ndb.BlobProperty();
    location = ndb.GeoPtProperty();

class Artist(EndpointsModel):
    fname = ndb.StringProperty();
    lname = ndb.StringProperty();
    website_url = ndb.StringProperty();
    description = ndb.StringProperty();

class Comment(EndpointsModel):
    sculpture_key = ndb.StringProperty();
    author = ndb.StringProperty();
    content = ndb.StringProperty();
    timestamp = ndb.DateTimeProperty(auto_now=True);
    
    
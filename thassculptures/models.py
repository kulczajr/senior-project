from google.appengine.ext import ndb


class Sculpture(ndb.Model):
    title = ndb.StringProperty();
    artist = ndb.KeyProperty();
    description = ndb.StringProperty();
    image = ndb.BlobProperty();
    location = ndb.GeoPtProperty();

class Artist(ndb.Model):
    fname = ndb.StringProperty();
    lname = ndb.StringProperty();
    website_url = ndb.StringProperty();
    description = ndb.StringProperty();

class Comment(ndb.Model):
    author = ndb.StringProperty();
    content = ndb.StringProperty();
    timestamp = ndb.DateTimeProperty(auto_now=True);
    
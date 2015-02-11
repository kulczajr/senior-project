import os
import pprint

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import ndb
from models import Sculpture, Artist, Comment
import jinja2
import webapp2

'''
Instructions:
Start google app engine server,
go to http://localhost:8000/console
paste into interactive console
click the blue 'Execute' button


'''
pprint.pprint(os.environ.copy())
ARTIST_KEY = ndb.Key("Entity", "artist_root")
new_artist = Artist(parent = ARTIST_KEY, 
                                   fname = "fname", 
                                   lname = "lname", 
                                   website_url = "website_url", 
                                   description = "description")
new_artist.put()
SCULPTURE_KEY = ndb.Key("Entity", "sculpture_root")
new_sculpture = Sculpture(parent = SCULPTURE_KEY,
                                      title = "title",
                                      artist = new_artist.key,
                                      location = db.GeoPt(55,55),
                                      description = "description",
                                      image = "image")
new_sculpture.put()
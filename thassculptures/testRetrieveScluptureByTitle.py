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
pprint.pprint(os.environ.copy())
qry1= Sculpture.query(Sculpture.title == "title");
print qry1.get().description
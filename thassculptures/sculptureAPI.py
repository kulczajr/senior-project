import os
import pprint

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import ndb
from models import Sculpture, Artist, Comment

@endpoints.api(name='Sculpture', version='v1')
class SculptureApi
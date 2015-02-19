#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from google.appengine.ext import ndb
from models import Sculpture, Artist, Comment
import jinja2
import webapp2

import pprint

from apiclient.discovery import build


SCULPTURE_KEY = ndb.Key("Entity", "sculpture_root")
ARTIST_KEY = ndb.Key("Entity", "artist_root")
COMMENT_KEY = ndb.Key("Entity", "comment_root")

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

api_root = 'https://thassculptures.appspot.com/_ah/api'
api = 'sculptures'
version = 'v1'
discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
service = build(api, version, discoveryServiceUrl=discovery_url)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/index.html")
        self.response.write(template.render())

        
class MobileTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture = {
            'title':"Flame of the Millennium",
            'artist':"Leonard Nierman",
            'description': "Flame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of Technology, was the first sculpture in the Art Spaces collection. Its impressive form gives over to large gleaming surfaces which mirror the reflecting pool surrounding it, and offer a spectacle of changing colors and patterns for motorists along Historic National Road U.S. 40 as it enters Terre Haute. Artist Leonardo Nierman lives in Mexico City and works in a variety of media including paint, stained glass and tapestry, but most of his large scale outdoor works are stainless steel, as is the Flame. His education in physics and mathematics and his study of the psychology of color and music have helped to shape his artistic style. What is common to all of his works is the lively and uplifting spirit that inhabits his forms and the vibrancy of the material as it moves skyward.",
            'image':"Some pretty picture",  # not quite sure how to handle images with Jinja yet... will look in to
            'audio': "ToDo",
            'location':"GeoPage"
        }
        self.response.write(template.render(sculpture))

class fourHundredChar(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture = {
            'title':"Flame of the Millennium",
            'artist':"Leonard Nierman",
            'description': "Artist Leonardo Nierman lives in Mexico City and works in a variety of media including paint, stained glass and tapestry, but most of his large scale outdoor works are stainless steel, as is the Flame. His education in physics and mathematics and his study of the psychology of color and music have helped to shape his artistic style. What is common to all of his works is the lively and uplifting spirit that inhabits his forms and the vibrancy of the material as it moves skywar",
            'image':"Some pretty picture",  # not quite sure how to handle images with Jinja yet... will look in to
            'audio': "ToDo",
            'location':"GeoPage"
        }
        self.response.write(template.render(sculpture))

class eightHundredChar(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture = {
            'title':"Flame of the Millennium",
            'artist':"Leonard Nierman",
            'description': "Flame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of Technology, was the first sculpture in the Art Spaces collection. Its impressive form gives over to large gleaming surfaces which mirror the reflecting pool surrounding it, and offer a spectacle of changing colors and patterns for motorists along Historic National Road U.S. 40 as it enters Terre Haute. Artist Leonardo Nierman lives in Mexico City and works in a variety of media including paint, stained glass and tapestry, but most of his large scale outdoor works are stainless steel, as is the Flame. His education in physics and mathematics and his study of the psychology of color and music have helped to shape his artistic style. What is common to all of his works is the lively and uplifting.",
            'image':"Some pretty picture",  # not quite sure how to handle images with Jinja yet... will look in to
            'audio': "ToDo",
            'location':"GeoPage"
        }
        self.response.write(template.render(sculpture))

class twelveHundredChar(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture = {
            'title':"Flame of the Millennium",
            'artist':"Leonard Nierman",
            'description': "Flame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of Technology, was the first sculpture in the Art Spaces collection. Its impressive form gives over to large gleaming surfaces which mirror the reflecting pool surrounding it, and offer a spectacle of changing colors and patterns for motorists along Historic National Road U.S. 40 as it enters Terre Haute. Artist Leonardo Nierman lives in Mexico City and works in a variety of media including paint, stained glass and tapestry, but most of his large scale outdoor works are stainless steel, as is the Flame. His education in physics and mathematics and his study of the psychology of color and music have helped to shape his artistic style. What is common to all of his works is the lively and uplifting spFlame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of TechnFlame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of TechnFlame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of TechnFlame of the Millennium by Leonardo Nierman, located on the campus of Rose-Hulman Institute of Techn.",
            'image':"Some pretty picture",  # not quite sure how to handle images with Jinja yet... will look in to
            'audio': "ToDo",
            'location':"GeoPage"
        }
        self.response.write(template.render(sculpture))

class SculpturesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptures.html")
        
        # Fetch all greetings and print them out.
        response = service.sculpture().list().execute()
        # sculptures_query = Sculpture.query(ancestor=SCULPTURE_KEY)
        self.response.write(template.render({'response': response['items']}))
class SculptureCardHandler(webapp2.RequestHandler):
    def post(self):
        template = jinja_env.get_template("web/single-page.html")
        sculpture_title = self.request.get("sculpture-title")
        sculptures = service.sculpture().list().execute()
        sculpture_for_card = None
        for sculpture in sculptures['items']:
            if sculpture['title'] == sculpture_title:
                sculpture_for_card = sculpture
                break
        self.response.write(template.render({'sculpture':sculpture_for_card}))
        
class MapHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/map.html")
        self.response.write(template.render())
class ArtistsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/artists.html")
        self.response.write(template.render())
class AddSculptureHandler(webapp2.RequestHandler):
    def post(self):
        # The non-string attributes probably are going to need changing here,
        # but I don't know how to handle them yet.
        
        # Also, a general gist of what's happening here:
        # We check to see if the statue already exists.
        # If it does, we're updating it.
        # If it doesn't, we're creating a new one and adding it.
        # It checks the request for an entity key, which is what
        # it would contain if the sculpture exists.
        new_sculpture = Sculpture(title=self.request.get("title"),
                                  artist=None,
                                  location=None,
                                  description=self.request.get("description"),
                                  image=None)
        new_sculpture.put()
        self.redirect(self.request.referer)

class AddArtistHandler(webapp2.RequestHandler):
    def post(self):
        new_artist = Artist(fname=self.request.get("fname"),
                               lname=self.request.get("lname"),
                               website_url=self.request.get("website_url"),
                               description=self.request.get("description"))
        new_artist.put()
        self.redirect(self.request.referer)

class AddCommentHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.get("entity_key"):
            comment_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            comment = comment_key.get()
            comment.author = self.request.get("author")
            comment.content = self.request.get("content")
            comment.put()
        else:
            new_comment = Comment(parent=COMMENT_KEY,
                                   author=self.request.get("author"),
                                   content=self.request.get("content"))
            new_comment.put()
        self.redirect(self.request.referer)

class AddArtistPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddArtist.html")
        # new_artist = Artist(fname = "WHAT", 
        #               lname = "IS", 
        #               website_url = "GOING", 
        #               description = "ON")
        # service.artist().insert(new_artist)
        self.response.write(template.render())
    def post(self):
        new_artist = Artist(fname=self.request.get("fname"),
                               lname=self.request.get("lname"),
                               website_url=self.request.get("website_url"),
                               description=self.request.get("description"))
        new_artist.put()
        self.redirect(self.request.referer)        

class AddSculpturePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddSculpture.html")
        self.response.write(template.render())
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sculptures.html', SculpturesHandler),
    ('/single-page.html', SculptureCardHandler),
    ('/fourhundred.html', fourHundredChar),
    ('/eighthundred.html', eightHundredChar),
    ('/twelvehundred.html', twelveHundredChar),
    ('/mobile-test.html', MobileTestHandler),
    ('/addSculpture', AddSculptureHandler),
    ('/addArtist', AddArtistHandler),
    ('/addComment', AddCommentHandler),
    ('/map.html', MapHandler),
    ('/artists.html', ArtistsHandler),
    ('/addArtistPage', AddArtistPageHandler),
    ('/addSculpturePage', AddSculpturePageHandler),
], debug=True)

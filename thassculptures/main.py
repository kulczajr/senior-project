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


SCULPTURE_KEY = ndb.Key("Entity", "sculpture_root")
ARTIST_KEY = ndb.Key("Entity", "artist_root")
COMMENT_KEY = ndb.Key("Entity", "comment_root")

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/index.html")
        self.response.write(template.render())

class SculpturesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptures.html")
        self.response.write(template.render())
class SculptureCardHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/single-page.html")
        self.response.write(template.render())
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
        #The non-string attributes probably are going to need changing here,
        #but I don't know how to handle them yet.
        
        #Also, a general gist of what's happening here:
        #We check to see if the statue already exists.
        #If it does, we're updating it.
        #If it doesn't, we're creating a new one and adding it.
        #It checks the request for an entity key, which is what
        #it would contain if the sculpture exists.
        if self.request.get("entity_key"):
            sculpture_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            sculpture = sculpture_key.get()
            sculpture.title = self.request.get("title")
            sculpture.artist = self.request.get("artist")
            sculpture.location = self.request.get("location")
            sculpture.description = self.request.get("description")
            sculpture.image = self.request.get("image")
            sculpture.put()
        else:
            new_sculpture = Sculpture(parent = SCULPTURE_KEY,
                                      title = self.request.get("title"),
                                      artist = self.request.get("artist"),
                                      location = self.request.get("location"),
                                      description = self.request.get("description"),
                                      image = self.request.get("image"))
            new_sculpture.put()
        self.redirect(self.request.referer)

class AddArtistHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.get("entity_key"):
            artist_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            artist = artist_key.get()
            artist.fname = self.request.get("fname")
            artist.lname = self.request.get("lname")
            artist.website_url = self.request.get("website_url")
            artist.description = self.request.get("description")
            artist.put()
        else:
            new_artist = Artist(parent = ARTIST_KEY, 
                                   fname = self.request.get("fname"), 
                                   lname = self.request.get("lname"), 
                                   website_url = self.request.get("website_url"), 
                                   description = self.request.get("description"))
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
            new_comment = Comment(parent = COMMENT_KEY, 
                                   author = self.request.get("author"), 
                                   content = self.request.get("content"))
            new_comment.put()
        self.redirect(self.request.referer)

class AddArtistPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddArtist.html")
        self.response.write(template.render())

class AddSculpturePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddSculpture.html")
        self.response.write(template.render())
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sculptures.html', SculpturesHandler),
    ('/single-page.html', SculptureCardHandler),
    ('/addSculpture', AddSculptureHandler),
    ('/addArtist', AddArtistHandler),
    ('/addComment', AddCommentHandler),
    ('/map.html', MapHandler),
    ('/artists.html', ArtistsHandler),
    ('/addArtistPage', AddArtistPageHandler),
    ('/addSculpturePage', AddSculpturePageHandler),
], debug=True)

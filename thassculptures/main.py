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
import time
import json
import pprint
import re
import datetime
from apiclient.discovery import build
from google.appengine._internal.django.utils.safestring import mark_safe
from google.storage.speckle.proto.jdbc_type import NULL


SCULPTURE_KEY = ndb.Key("Entity", "sculpture_root")
ARTIST_KEY = ndb.Key("Entity", "artist_root")
COMMENT_KEY = ndb.Key("Entity", "comment_root")
TOLERANCE = .001

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

class SculpturesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/sculptures.html")
        
        # Fetch all greetings and print them out.
        response = service.sculpture().list(limit=50).execute()
        # sculptures_query = Sculpture.query(ancestor=SCULPTURE_KEY)
        self.response.write(template.render({'response': response['items']}))

class SculptureCardHandler(webapp2.RequestHandler):
    def post(self):
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture_title = self.request.get("sculpture-title")
        sculptures = service.sculpture().list().execute()
        comments = service.comment().list().execute()
        sculpture_for_card = None
        comments_for_card = []
        for sculpture in sculptures['items']:
            if sculpture['title'] == sculpture_title:
                sculpture_for_card = sculpture
                for comment in comments['items']:
                    if comment['sculpture_key'] == sculpture_for_card["entityKey"]:
                        comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'comments':comments_for_card}))


class DirectionsHandler(webapp2.RequestHandler):
    def post(self):
        template = jinja_env.get_template("web/directions.html")
        sculpture_title = self.request.get("sculpture_title")
        sculpture_location = self.request.get("location")
        self.response.write(template.render({'title':sculpture_title, 'location':sculpture_location}))

class MapHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/map.html")
		
        # Fetch all sculptures, put them into template
        response = service.sculpture().list().execute()
        self.response.write(template.render({'response': response['items']}))
		
class MapHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/map.html")
		
        # Fetch all sculptures, put them into template
        response = service.sculpture().list().execute()
        self.response.write(template.render({'response': response['items']}))

class ArtistsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/artists.html")
        self.response.write(template.render())
    def post(self):
        artists = service.artist().list().execute()
        template = jinja_env.get_template("web/artists.html")
        sculpture = self.request.get("sculpture_title")
        artistName = self.request.get("artistName")
        artistToFetch = None
        for artist in artists['items']:
            if artist['fname'] + " " + artist['lname'] == artistName:
                artistToFetch = artist
        self.response.write(template.render({'artist':artistToFetch, 'referringSculpture':sculpture}))
        
class AddSculptureHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddSculpture.html")
        self.response.write(template.render())
        
    def post(self):
        #Also, a general gist of what's happening here:
        #We check to see if the statue already exists.
        #If it does, we're updating it.
        #If it doesn't, we're creating a new one and adding it.
        #It checks the request for an entity key, which is what
        #it would contain if the sculpture exists.
        latitude = self.request.get("latitude")
        longitude = self.request.get("longitude")
        location = latitude + ", " + longitude
        new_sculpture = Sculpture(title = self.request.get("title"),
                                  artist = self.request.get("artist"),
                                  location = location,
                                  description = self.request.get("description"),
                                  image = self.request.get("image"))
        new_sculpture.put()
        self.redirect(self.request.referer)


class AddCommentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddComment.html")
        self.response.write(template.render())

    def post(self):
        new_comment = Comment(author=self.request.get("addCommentAuthor"),
                              sculpture_key = self.request.get("sculpture_key"),
                              content=self.request.get("addCommentBody"))
        new_comment.put()
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture_title = self.request.get("sculpture_title")
        sculptures = service.sculpture().list().execute()
        comments = service.comment().list().execute()
        sculpture_for_card = None
        comments_for_card = []
        for sculpture in sculptures['items']:
            if sculpture['title'] == sculpture_title:
                sculpture_for_card = sculpture
                for comment in comments['items']:
                    if comment['sculpture_key'] == sculpture_for_card["entityKey"]:
                        if comment['is_approved']:
                            comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'comments':comments_for_card}))


class AddArtistHandler(webapp2.RequestHandler):
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

class MyLocationHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/my_location.html")
        sculptures = service.sculpture().list().execute()
        sculpture_items = sculptures['items']
        json_test = self.parse_for_json()
        print json_test
        print sculpture_items
        self.response.write(template.render({'sculptures' : sculpture_items}))

    def parse_for_json(self):
        return "parse_magic"
        
class CheckForStatueHandler(webapp2.RequestHandler):
    def post(self):
        sculptures = service.sculpture().list().execute()
        #sculptures = Sculpture.query()
        print "got here!"
        current_x = float(self.request.get("x_coord"))
        current_y = float(self.request.get("y_coord"))
        #current_x = 75
        #current_y = 75
        print current_x
        print current_y
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        for sculpture in sculptures['items']:
            sculpture_x = float(self.get_x(sculpture['location']))
            sculpture_y = float(self.get_y(sculpture['location']))
            print sculpture_x
            print sculpture_y
            if self.is_by_statue(sculpture_x, sculpture_y, current_x, current_y):
                print "You're by a statue!"
                sculpture_title = sculpture['title']
                #coordinates = {'sculpture_x' : sculpture_x, 'sculpture_y' : sculpture_y}
                self.response.out.write(json.dumps({"sculpture_title": sculpture_title}))
    
    def is_by_statue(self, sculpture_x, sculpture_y, current_x, current_y):
        print "sculpture_x is " + str(sculpture_x)
        print "sculpture_y is " + str(sculpture_y)
        print "current_x is " + str(current_x)
        print "current_y is " + str(current_y)
        return (abs(sculpture_x - current_x) < TOLERANCE and abs(sculpture_y - current_y) < TOLERANCE)
    
    def get_x(self, location):
        split_string = re.split(", ", location)
        return split_string[0]
    
    def get_y(self, location):
        split_string = re.split(", ", location)
        return split_string[1]
    
class CardFromLocationHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("sculpture_name")
        response = "Loading the card for " + name
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculpture_title = name
        sculptures = service.sculpture().list().execute()
        comments = service.comment().list().execute()
        sculpture_for_card = None
        comments_for_card = []
        for sculpture in sculptures['items']:
            if sculpture['title'] == sculpture_title:
                sculpture_for_card = sculpture
                for comment in comments['items']:
                    if comment['sculpture_key'] == sculpture_for_card["entityKey"]:
                        if comment['is_approved']:
                            comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'comments':comments_for_card}))
   
class AdminHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/admin.html")
        self.response.write(template.render())

class ApproveCommentsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/ApproveComments.html")
        comments = service.comment().list().execute()
        comments_for_card = []
        for comment in comments['items']:
            sculpture_key = ndb.Key(urlsafe=comment['sculpture_key'])
            sculpture = sculpture_key.get()       
            comment['sculpture'] = sculpture.title
            comments_for_card.append(comment)
        self.response.write(template.render({'comments':comments_for_card}))
class DenyComment(webapp2.RequestHandler):
    def post(self):
        comment = ''
class ApproveComment(webapp2.RequestHandler):
    def post(self):
        comment = ''
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/admin', AdminHandler),
    ('/ApproveComments', ApproveCommentsHandler),
    ("/DenyComment", DenyComment),
    ("/ApproveComment", ApproveComment),
    ('/sculptures.html', SculpturesHandler),
    ('/single-page.html', SculptureCardHandler),
    ('/addSculpture', AddSculptureHandler),
    ('/addArtist', AddArtistHandler),
    ('/addComment', AddCommentHandler),
    ('/map.html', MapHandler),
    ('/artist', ArtistsHandler),
    ('/my_location', MyLocationHandler),
    ('/CheckForStatue', CheckForStatueHandler),
    ('/CardFromLocation', CardFromLocationHandler),
    ('/directions.html', DirectionsHandler)
], debug=True)

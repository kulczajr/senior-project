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

from google.appengine.api import users
from google.appengine.ext import ndb
from models import Sculpture, Artist, Comment, Tour
import jinja2
import webapp2
import time
import json
import pprint
import re
import datetime
import urllib
import logging
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
logging.getLogger().setLevel(logging.DEBUG)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/index.html")
        self.response.write(template.render())

class MyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)

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
                    if comment["sculpture_key"] == sculpture_for_card["entityKey"]:
                        logging.debug(comment["is_approved"])
                        if comment['is_approved']:
                            comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'comments':comments_for_card}))

class DirectionsHandler(webapp2.RequestHandler):
    def post(self):
        template = jinja_env.get_template("web/directions.html")
        sculpture_title = self.request.get("sculpture-title")
        sculptures = service.sculpture().list().execute()
        dest_location = None
        for sculpture in sculptures['items']:
            if sculpture['title'] == sculpture_title:
                # note: do we need a case where we can't find the sculpture?
                dest_location = sculpture['location'];
        self.response.write(template.render({'title':sculpture_title, 'location': dest_location}))

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
        sculpture_title = self.request.get("sculpture_title")
        #artistName = self.request.get("artistName")
        #artistToFetch = None
        artist_key = ndb.Key(urlsafe=self.request.get("artist_key"))
        artist = artist_key.get()
        self.response.write(template.render({'artist':artist, 'referringSculpture':sculpture_title}))
        
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

        if self.request.get("entityKey"):
            sculpture_key = ndb.Key(urlsafe=self.request.get("entityKey"))
            sculpture = sculpture_key.get()       
            sculpture.title = self.request.get("title")
            sculpture.artist_key = self.request.get("artist_key")
            artist_key = ndb.Key(urlsafe=self.request.get("artist_key"))
            artist = artist_key.get()
            sculpture.artist = artist.fname + " " + artist.lname
            sculpture.location = location
            sculpture.description = self.request.get("description")
            sculpture.image = self.request.get("image")
            sculpture.think = self.request.get("think")
            sculpture.do = self.request.get("do")
            sculpture.put()
        else: 
            artist_key = ndb.Key(urlsafe=self.request.get("artist_key"))
            artist = artist_key.get()
            artist_name = artist.fname + " " + artist.lname
            new_sculpture = Sculpture(title = self.request.get("title"),
                                  artist = artist_name,
                                  artist_key = self.request.get("artist_key"),
                                  location = location,
                                  description = self.request.get("description"),
                                  think = self.request.get("think"),
                                  do = self.request.get("do"),
                                  image = self.request.get("image"))
            new_sculpture.put()
        self.redirect(self.request.referer)


class AddCommentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/AddComment.html")
        self.response.write(template.render())

    def post(self):
        jsonData = json.loads(self.request.body)
        new_comment = Comment(author=jsonData["addCommentAuthor"],
                              sculpture_key = jsonData["sculpture_key"],
                              content=jsonData["addCommentBody"],
                              is_approved=False)
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

class DeleteSculptureHandler(webapp2.RequestHandler):
    def post(self):
        sculpture_key = ndb.Key(urlsafe=self.request.get("entityKey"))
        sculpture = sculpture_key.get()       
        sculpture.key.delete();
        self.redirect(self.request.referer)

class AddArtistHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.get("entityKey"):
            artist_key = ndb.Key(urlsafe=self.request.get("entityKey"))
            artist = artist_key.get()       
            artist.fname = self.request.get("fname")
            artist.lname = self.request.get("lname")
            artist.image = self.request.get("image")
            artist.website_url = self.request.get("website_url")
            artist.description = self.request.get("description")
            artist.put()
        else: 
            new_artist = Artist(fname = self.request.get("fname"),
                                  lname = self.request.get("lname"),
                                  image = self.request.get("image"),
                                  website_url = self.request.get("website_url"),
                                  description = self.request.get("description"))
            new_artist.put()
        self.redirect(self.request.referer)

class ArtistAdminHandler(webapp2.RequestHandler):
    def get(self):
        artists = service.artist().list(limit=50).execute()
        template = jinja_env.get_template("web/ArtistAdminHub.html")
        self.response.write(template.render({'artists': artists['items']}))

class DeleteArtistHandler(webapp2.RequestHandler):
    def post(self):
        artist_key = ndb.Key(urlsafe=self.request.get("entityKey"))
        artist = artist_key.get()       
        artist.key.delete();
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
        sculptures = service.sculpture().list(limit=50).execute()
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
        user = users.get_current_user()
        if user:
            if user.nickname() == "wabashvalleyartspaces":
                sculptures = service.sculpture().list(limit=50).execute()
                artists = service.artist().list(limit=50).execute()
                template = jinja_env.get_template("web/admin.html")
                self.response.write(template.render({'sculptures': sculptures['items'], 'artists': artists['items']}))
            else:
                greeting = ('You cannot access this page as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
                self.response.out.write('<html><body>%s</body></html>' % greeting)
            
        else:
            greeting = ('<a href="%s">Sign in to access this page</a>.' %
                        users.create_login_url('/'))
            self.response.write(greeting)

class ToursAdminHandler(webapp2.RequestHandler):
    def get(self):
        sculptures = service.sculpture().list(limit=50).execute()
        tours = service.tour().list(limit=50).execute()
        template = jinja_env.get_template("web/ToursAdminHub.html")
        self.response.write(template.render({'sculptures': sculptures['items'], 'tours': tours['items']}))

class AddTourHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("web/ToursAdminHub.html")
        self.response.write(template.render())
        
    def post(self):
        selected_sculpture_key = ndb.Key(urlsafe=self.request.get("sculpture_list")) 
        selected_sculpture = selected_sculpture_key.get()
        sculpture_to_add = selected_sculpture.entityKey
        if self.request.get("entityKey"):
            tour_key = ndb.Key(urlsafe=self.request.get("entityKey"))
            tour = tour_key.get()       
            tour.description = self.request.get("description")
            selected_sculpture_key = ndb.Key(urlsafe=self.request.get("sculpture_list")) 
            selected_sculpture = selected_sculpture_key.get()
            sculpture_list = tour.sculpture_list
            sculpture_list.append(sculpture_to_add)
            tour.sculpture_list = sculpture_list
            tour.put()
        else:
            new_tour = Tour(description = self.request.get("description"),
                            sculpture_list = [sculpture_to_add]) 
            new_tour.put()
        self.redirect(self.request.referer)

        
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

class DenyCommentHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        comment = ndb.Key(urlsafe=data['commentKey']).get()
        comment.key.delete() #aaaaannnndddd it's gone. 

class ApproveCommentHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        comment = ndb.Key(urlsafe=data['commentKey']).get()
        comment.is_approved = True
        comment.put();

class SingleScultpureFinder(webapp2.RequestHandler):
    def get(self):
        name = self.request.get("sculpture-title")
        response = "Loading the card for " + name
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculptures = service.sculpture().list(limit=50).execute()
        comments = service.comment().list(limit=50).execute()
        sculpture_for_card = None
        artist_name_for_sculpture = None
        comments_for_card = []
        for sculpture in sculptures['items']:
            if sculpture['title'] == name:
                sculpture_for_card = sculpture
                artist_key_for_sculpture = sculpture.artist_key
                artist_for_sculpture = artist_key_for_sculpture.get()
                artist_name_for_sculpture = artist_for_sculpture.fname + " " + artist_for_sculpture.lname
                for comment in comments['items']:
                    if comment['sculpture_key'] == sculpture_for_card["entityKey"]:
                        if comment['is_approved']:
                            comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'artist_name':artist_name_for_sculpture, 'comments':comments_for_card}))
    def post(self):
        name = self.request.get("sculpture-title")
        response = "Loading the card for " + name
        template = jinja_env.get_template("web/sculptureCardTemplate.html")
        sculptures = service.sculpture().list(limit=50).execute()
        comments = service.comment().list(limit=50).execute()
        sculpture_for_card = None
        artist_name_for_sculpture = ""
        comments_for_card = []
        for sculpture in sculptures['items']:
            if sculpture['title'] == name:
                sculpture_for_card = sculpture
                if 'artist_key' in sculpture:
                    artist_key_for_sculpture = ndb.Key(urlsafe=sculpture['artist_key'])
                    artist_for_sculpture = artist_key_for_sculpture.get()
                    artist_name_for_sculpture = artist_for_sculpture.fname + " " + artist_for_sculpture.lname
                for comment in comments['items']:
                    if comment['sculpture_key'] == sculpture_for_card["entityKey"]:
                        if comment['is_approved']:
                            comments_for_card.append(comment)
                break
        self.response.write(template.render({'sculpture':sculpture_for_card, 'artist_name':artist_name_for_sculpture, 'comments':comments_for_card}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/admin', AdminHandler),
    ('/ApproveComments', ApproveCommentsHandler),
    ('/single-sculpture',SingleScultpureFinder),
    ("/DenyComment", DenyCommentHandler),
    ("/ApproveComment", ApproveCommentHandler),
    ('/sculptures.html', SculpturesHandler),
    ('/addSculpture', AddSculptureHandler),
    ('/deleteSculpture', DeleteSculptureHandler),
    ('/addArtist', AddArtistHandler),
    ('/addComment', AddCommentHandler),
    ('/map.html', MapHandler),
    ('/artist', ArtistsHandler),
    ('/my_location', MyLocationHandler),
    ('/CheckForStatue', CheckForStatueHandler),
    ('/CardFromLocation', CardFromLocationHandler),
    ('/DirectionsToStatue', DirectionsHandler),
    ('/ToursAdmin', ToursAdminHandler),
    ('/AddTour', AddTourHandler),
    ('/AddArtist', AddArtistHandler),
    ('/ArtistAdmin', ArtistAdminHandler),
    ('/deleteArtist', DeleteArtistHandler),
    ('/admin', AdminHandler)
], debug=True)

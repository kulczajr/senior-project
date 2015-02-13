'''
Created Feb 12, 2015

@author: songm
'''

import endpoints
import protorpc

from models import Sculpture, Artist, Comment

@endpoints.api(name="sculptures", version="v1", description="Sculpture API")
class SculptureApi(protorpc.remote.Service):
    
    @Sculpture.method(name="sculpture.insert", path="sculpture/insert", http_method="POST")
    def sculpture_insert(self, request):
        if request.from_datastore:
            my_quote = request
        else:
            my_quote = Sculpture(title=request.title, artist=request.artist, description=request.description, image=request.image, location=request.location)
        my_quote.put()
        return my_quote
    
    @Sculpture.query_method(name="sculpture.list", path="sculpture/list", http_method="GET", query_fields=("limit", "order", "pageToken"))
    def sculpture_list(self, query):
        return query
    
    @Sculpture.method(name="sculpture.delete", path="sculpture/delete/{entityKey}", http_method="DELETE", request_fields=("entityKey",))
    def sculpture_delete(self, request):
        if not request.from_datastore:
            raise endpoints.NotFoundException("KEY NOT FOUND")
        else:
            request.key.delete()
            
        return Sculpture(quote="deleted")

    @Artist.method(name="artist.insert", path="artist/insert", http_method="POST")
    def artist_insert(self, request):
        if request.from_datastore:
            my_quote = request
        else:
            my_quote = Artist(fname=request.fname, lname=request.lname, website_url=request.website_url, description=request.description)
            
        my_quote.put()
        return my_quote
    
    @Artist.query_method(name="artist.list", path="artist/list", http_method="GET", query_fields=("limit", "order", "pageToken"))
    def artist_list(self, query):
        return query
    
    @Artist.method(name="artist.delete", path="artist/delete/{entityKey}", http_method="DELETE", request_fields=("entityKey",))
    def artist_delete(self, request):
        if not request.from_datastore:
            raise endpoints.NotFoundException("KEY NOT FOUND")
        else:
            request.key.delete()
            
        return Artist(quote="deleted")
    
    @Comment.method(name="comment.insert", path="comment/insert", http_method="POST")
    def comment_insert(self, request):
        if request.from_datastore:
            my_quote = request
        else:
            my_quote = Comment(sculpture_key=request.sculpture_key, author=request.author, content=request.content)
            
        my_quote.put()
        return my_quote
    
    @Comment.query_method(name="comment.list", path="comment/list", http_method="GET", query_fields=("limit", "order", "pageToken"))
    def comment_list(self, query):
        return query
    
    @Comment.method(name="comment.delete", path="comment/delete/{entityKey}", http_method="DELETE", request_fields=("entityKey",))
    def comment_delete(self, request):
        if not request.from_datastore:
            raise endpoints.NotFoundException("KEY NOT FOUND")
        else:
            request.key.delete()
            
        return Comment(quote="deleted")

app = endpoints.api_server([SculptureApi], restricted=False)

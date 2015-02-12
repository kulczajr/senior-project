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



app = endpoints.api_server([SculptureApi], restricted=False)

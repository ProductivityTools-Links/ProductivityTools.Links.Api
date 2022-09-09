
from Models.Links import Links
from Models.Relation import Relation
from flask import request, Response
import jsonpickle


from Resources.ApiResource import ApiResource

class LinkListResource(ApiResource):

    def get(self,id):
        link = Links(self.uri, self.user, self.password)
        result=link.getLinks(id)
        link.close()
        jsonresult=jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)


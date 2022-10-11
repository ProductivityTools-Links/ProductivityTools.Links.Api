
from Models.Links import Links
from Models.Relation import Relation
from flask import request, Response
import jsonpickle


from Resources.ApiResource import ApiResource

class TreeLinkListResource(ApiResource):
    def get(self,login):
        link = Links(self.uri, self.user, self.password)
        result=link.getTreeLinks(login)
        link.close()
        jsonresult=jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)



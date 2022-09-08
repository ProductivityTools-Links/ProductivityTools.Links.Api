
from Models.Links import Links
from Models.Relation import Relation
from flask import request, Response
import jsonpickle


from Resources.ApiResource import ApiResource

class Link2Resource(ApiResource):

    def get(self,id):
        link = Links(self.uri, self.user, self.password)
        result=link.getLinks(id)
        link.close()
        jsonresult=jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)

    def post(self):
        parentId=request.json['parentId']
        name=request.json['name']
        url=request.json['url']
        description=request.json['description']

        link=Links(self.uri,self.user,self.password)
        createdLinkId=link.create(name,url,description)
        link.close()

        relation=Relation(self.uri,self.user,self.password)
        relation.create(parentId,createdLinkId)
        relation.close();
        return Response(str(createdLinkId), mimetype="text/plain", direct_passthrough=True);



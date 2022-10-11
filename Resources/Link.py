
from Models.Links import Links
from Models.Relation import Relation
from flask import request, Response
import jsonpickle


from Resources.ApiResource import ApiResource

class LinkResource(ApiResource):
    def post(self):
        message = ApiResource.check_authorization(self)
        if (message != None):
            return message, 401

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
        return Response(str(createdLinkId), mimetype="text/plain", direct_passthrough=True)


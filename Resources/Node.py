
from Models.Link import Link
from Models.Relation import Relation
from flask import request, Response

from Resources.ApiResource import ApiResource

class NodeResource(ApiResource):
    def post(self):
        parentId=5
        name=request.json['name']
        url=request.json['url']
        description=request.json['description']

        link=Link(self.uri,self.user,self.password)
        createdLinkId=link.create(name,url,description)
        link.close()

        relation=Relation(self.uri,self.user,self.password)
        relation.create(parentId,createdLinkId)
        relation.close();
        return Response(str(createdLinkId), mimetype="text/plain", direct_passthrough=True);



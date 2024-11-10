
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

        id = request.json.get("id")
        parentId=request.json['parentId']
        name=request.json['name']
        url=request.json['url']
        description=request.json['description']
        authors=request.json['authors']

        link=Links(self.uri,self.user,self.password)
        if id is None:
            createdLinkId=link.create(name,url,description,authors)
            relation = Relation(self.uri, self.user, self.password)
            relation.create(parentId, createdLinkId)
            relation.close();
            link.close()
            return Response(str(createdLinkId), mimetype="text/plain", direct_passthrough=True)

        else:
            link.update(id,name,url,description,authors)
            return Response(str("updated"), mimetype="text/plain", direct_passthrough=True)
    def delete(self):
        id=request.json.get("id")
        link=Links(self.uri,self.user,self.password)
        result=link.delete(id);
        return Response(str("deleted $id"), mimetype="text/plain", direct_passthrough=True)




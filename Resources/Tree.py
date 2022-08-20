from flask_restful import Resource
from flask import Response, request, jsonify
from Models.Node import Node
from Models.Relation import Relation
from Models.Tree import Tree
import json
from Resources.ApiResource import ApiResource

class TreeResource(ApiResource):
    def get(self):
        tree = Tree(self.uri, self.user, self.password)
        result=tree.getTree("pwujczyk1")
        tree.close()
        jsonresult=json.dumps(result)
        return jsonify(result)
       #return Response("ok", mimetype="text/plain", direct_passthrough=True);

    def post(self):
        nodeName=request.json['name']
        node = Node(self.uri, self.user, self.password)
        createdNodeId=node.create(nodeName);
        node.close();
        relation=Relation(self.uri,self.user,self.password);
        relation.create(37,createdNodeId)
        relation.close();
        return Response(str(createdNodeId), mimetype="text/plain", direct_passthrough=True);

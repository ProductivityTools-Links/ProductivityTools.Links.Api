from flask_restful import Resource
from flask import Response, request
from Models.Node import Node
from Models.Relation import Relation
import os
from Resources.ApiResource import ApiResource

class TreeResource(ApiResource):
    def get(self):
        uri = "neo4j+s://8345876f.databases.neo4j.io"
        user = "neo4j"
        password = os.getenv('password')
        #password = "Kp9gl8g7YWx9XDrqAW"
        node = Node(uri, user, password)
        #app.create_friendship("Alice1", "David")
        x=node.create("Alice")
        node.close()

        relation=Relation(uri, user, password)
        relation.create(1,x);

        return Response(str(x), mimetype="text/plain", direct_passthrough=True);

    def post(self):
        nodeName=request.json['name']
        node = Node(self.uri, self.user, self.password)
        createdNodeId=node.create(nodeName);
        node.close();
        relation=Relation(self.uri,self.user,self.password);
        relation.create(37,createdNodeId)
        relation.close();
        return Response(str(createdNodeId), mimetype="text/plain", direct_passthrough=True);

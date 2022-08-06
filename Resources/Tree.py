from flask_restful import Resource
from flask import Response
from Models.Node import Node
from Models.Relation import Relation
import os

class TreeResource(Resource):
    def get(self):
        uri = "neo4j+s://8345876f.databases.neo4j.io"
        user = "neo4j"
        password = os.getenv('password')
        #password = "Kp9gl8g7YWx9XDrqAW"
        node = Node(uri, user, password)
        #app.create_friendship("Alice1", "David")
        x=node.create(1, "Alice")
        node.close()

        relation=Relation(uri, user, password)
        relation.create(1,x);

        return Response(str(x), mimetype="text/plain", direct_passthrough=True);
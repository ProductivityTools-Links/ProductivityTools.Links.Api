from flask_restful import Resource
from flask import Response
from Models.Node import Node
import os

class NodeResource(Resource):
    def get(self):
        uri = "neo4j+s://8345876f.databases.neo4j.io"
        user = "neo4j"
        password = os.getenv('password')
        #password = "Kp9gl8g7YWx9XDrqAW"
        app = Node(uri, user, password)
        #app.create_friendship("Alice1", "David")
        x=app.create(1, "Alice")
        app.close()



        return Response("fdsa");
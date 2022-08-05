from flask_restful import Resource
from flask import Response
from Models.Tree import Tree
import os

class TreeResource(Resource):
    def get(self):
        uri = "neo4j+s://8345876f.databases.neo4j.io"
        user = "neo4j"
        password = os.getenv('password')
        #password = "Kp9gl8g7YWx9XDrqAW"
        app = Tree(uri, user, password)
        app.create_friendship("Alice", "David")
        app.find_person("Alice")
        app.close()



        return Response("fdsa");
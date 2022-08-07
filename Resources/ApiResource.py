from flask_restful import Resource
import os

class ApiResource(Resource):
    def __init__(self):
        self.uri= "neo4j+s://8345876f.databases.neo4j.io"
        self.user = "neo4j"
        self.password = os.getenv('password')
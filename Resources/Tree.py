from flask_restful import Resource
from flask import Response

class TreeResource(Resource):
    def get(self):
        return Response("fdsa");
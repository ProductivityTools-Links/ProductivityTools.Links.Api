from Resources.Tree import TreeResource
from flask import  Flask
from flask_restful import Api

def create_app():
    app=Flask(__name__)
    register_resources(app)

def register_resources(app):
    api=Api(app)
    api.add_resource(TreeResource,'/Tree')
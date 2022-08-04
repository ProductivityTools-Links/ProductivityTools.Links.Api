from Resources.Date import DateResource
from Resources.Tree import TreeResource
from flask import Flask
import os
from flask_restful import Api

def create_app():
    app=Flask(__name__)
    register_resources(app)
    return app

def register_resources(app):
    api=Api(app)
    api.add_resource(DateResource,'/Date')
    api.add_resource(TreeResource,'/Tree')


if __name__=="__main__":
    app=create_app()
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
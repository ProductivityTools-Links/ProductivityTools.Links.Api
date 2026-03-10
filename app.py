from Resources.Date import DateResource
from Resources.Tree import TreeResource
from Resources.Account import AccountResource
from Resources.LinkList import LinkListResource
from Resources.Link import LinkResource
from Resources.Relation import RelationResoure
from Resources.Password import PasswordResource
from Resources.AccountList import AccountListResource
from Resources.TreeLinkList import TreeLinkListResource
from flask import Flask
import os
from flask_restful import Api
from flask_cors  import CORS
from firebase_admin import initialize_app

def create_app():
    app=Flask(__name__)
    # Explicitly allow Authorization header and common methods
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Authorization", "Content-Type"]}})
    register_resources(app)
    default_app = initialize_app()
    return app

def register_resources(app):
    api=Api(app)
    api.add_resource(AccountResource,'/account', '/Account')
    api.add_resource(AccountListResource,'/accountlist', '/AccountList')
    api.add_resource(DateResource,'/date', '/Date')
    api.add_resource(TreeResource,'/tree', '/Tree')
    api.add_resource(LinkResource,'/link', '/Link')
    api.add_resource(LinkListResource, '/link/<int:id>', '/Link/<int:id>')
    api.add_resource(TreeLinkListResource, '/treelinks/<string:login>', '/TreeLinks/<string:login>')
    api.add_resource(RelationResoure, '/relation', '/Relation')
    api.add_resource(PasswordResource,'/password', '/Password')


if __name__=="__main__":
    app=create_app()
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
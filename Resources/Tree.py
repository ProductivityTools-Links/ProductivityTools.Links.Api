from flask_restful import Resource
from flask import Response, request, jsonify
from Models.Node import Node
from Models.Relation import Relation
from Models.Tree import Tree
from Models.Account import Account
import json
import jsonpickle
from json import JSONEncoder
from http import HTTPStatus


from Resources.ApiResource import ApiResource

class TreeResource(ApiResource):
    def get(self):

        if self.validate_token() == False:
            return {'message': 'access token is incorrect'}, HTTPStatus.UNAUTHORIZED

        accountName='pwujczyk1'
        #move it to login
        account =Account(self.uri,self.user,self.password)
        accountExists=account.checkIfAccountCreated(accountName)
        print(accountExists);
        if (accountExists==False):
            account.create(accountName)


        tree = Tree(self.uri, self.user, self.password)
        result=tree.getTree("pwujczyk1")
        tree.close()
        jsonresult=jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)
        return jsonresult
       # return Response("ok", mimetype="text/plain", direct_passthrough=True);

    def post(self):
        parentId = request.json['parentId']
        nodeName=request.json['name']
        node = Node(self.uri, self.user, self.password)
        createdNodeId=node.create(nodeName);
        node.close();
        relation=Relation(self.uri,self.user,self.password);
        relation.create(parentId,createdNodeId)
        relation.close();


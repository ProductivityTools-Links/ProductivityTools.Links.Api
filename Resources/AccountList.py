from flask_restful import Resource
import os
from flask import Response
from Models.Account import Account
import jsonpickle


from Resources.ApiResource import ApiResource

class AccountListResource(ApiResource):


    def get(self):
        # uri = "neo4j+s://8345876f.databases.neo4j.io"
        # user = "neo4j"
        # password = os.getenv('password')
        # password = "Kp9gl8g7YWx9XDrqAW"
        app = Account(self.uri, self.user, self.password)
        # app.create_friendship("Alice1", "David")
        result = app.getList()
        jsonresult = jsonpickle.encode(result, unpicklable=False)
        app.close()
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)


from flask_restful import Resource
import os
from flask import Response, request
from Models.Account import Account
import jsonpickle
from firebase_admin import auth


from Resources.ApiResource import ApiResource

class AccountListResource(ApiResource):


    def get(self):


        if('HTTP_AUTHORIZATION' in  request.headers.environ):
            id_token = request.headers.environ['HTTP_AUTHORIZATION']
            id_token = id_token.replace("Bearer", "")
            id_token = id_token.replace(" ", "")
        else:
            response = jsonpickle.encode({'message': 'Missing Http_Authorization header'})
            return response, 401

        if id_token=='null':
            return {'message': 'Missing Http_Authorization header'}, 401

        try:
            decoded_token = auth.verify_id_token(id_token)
        except BaseException as e:
            return {'message':str(e) }, 401

        email=decoded_token['email']
        if (email.endswith('google.com')==False):
            response = {'message': 'Only Googlers'}
            return response, 401


        app = Account(self.uri, self.user, self.password)
        # app.create_friendship("Alice1", "David")
        result = app.getList()
        jsonresult = jsonpickle.encode(result, unpicklable=False)
        app.close()
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)


from flask_restful import Resource
import os
from google.cloud import secretmanager
from flask import request, Response


class PasswordResource(Resource):
    def get(self):
        client=secretmanager.SecretManagerServiceClient()
        name=""
        r=client.access_secret_version(request={"name":name})
        return Response(str(r), mimetype="text/plain", direct_passthrough=True);

from flask_restful import Resource
import os
from google.cloud import secretmanager
from flask import request, Response


class PasswordResource(Resource):
    def get(self):
        return Response("password", mimetype="text/plain", direct_passthrough=True);
        # client=secretmanager.SecretManagerServiceClient()
        # name="projects/488456392633/secrets/neo4jpassword/versions/1"
        # r=client.access_secret_version(request={"name":name})
        # x=str(r.payload.data.decode("UTF-8")).strip()[4:-1]
        # return Response(str(x), mimetype="text/plain", direct_passthrough=True);

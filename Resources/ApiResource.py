from flask_restful import Resource
from flask import request
import os
from google.cloud import secretmanager
from firebase_admin import auth


class ApiResource(Resource):

    def getPassword(self):
        client = secretmanager.SecretManagerServiceClient()
        name = "projects/488456392633/secrets/neo4jpassword/versions/1"
        r = client.access_secret_version(request={"name": name})
        x = str(r.payload.data.decode("UTF-8")).strip()[4:-1]
        return x

    def __init__(self):
        devUri="neo4j+s://ae7a9693.databases.neo4j.io";
        prodUri="neo4j+s://8345876f.databases.neo4j.io";

        self.uri = devUri
        self.password=os.getenv('password')
        if self.password is None:
       # if True:
            self.password= self.getPassword();
            self.uri=prodUri

        self.user = "neo4j"

    def validate_token(self):
        if request.headers.environ.__contains__('HTTP_AUTHORIZATION') ==False:
            return False;
        id_token = request.headers.environ['HTTP_AUTHORIZATION']
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")
        if id_token == 'null':
            return False
        decoded_token = auth.verify_id_token(id_token)
        print(decoded_token);
        x=decoded_token
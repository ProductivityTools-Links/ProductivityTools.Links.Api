from flask_restful import Resource
import os
from google.cloud import secretmanager

class ApiResource(Resource):

    def getPassword(self):
        client = secretmanager.SecretManagerServiceClient()
        name = "projects/488456392633/secrets/neo4jpassword/versions/1"
        r = client.access_secret_version(request={"name": name})
        x = str(r.payload.data.decode("UTF-8")).strip()[4:-1]
        return x

    def __init__(self):
        self.uri= "neo4j+s://8345876f.databases.neo4j.io"
        self.user = "neo4j"
        #self.password = os.getenv('password')
        self.password = self.getPassword(self);
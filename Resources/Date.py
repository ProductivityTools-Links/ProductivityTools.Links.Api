from flask_restful import Resource
from datetime import datetime
from flask import Response

class DateResource(Resource):
    def get(self):
        now=datetime.now();
        dts = now.strftime("%d/%m/%Y %H:%M:%S")
        return Response(dts, mimetype="text/plain", direct_passthrough=True)
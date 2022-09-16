from http import HTTPStatus
from flask import request

from Models.Relation import Relation
from Resources.ApiResource import  ApiResource

class RelationResoure(ApiResource):
    def post(self):
        id = request.json['id']
        targetParentId = request.json['targetParentId']
        relation = Relation(self.uri, self.user, self.password)
        relation.remove(id)
        relation.create(targetParentId,id);
        return {}, HTTPStatus.OK

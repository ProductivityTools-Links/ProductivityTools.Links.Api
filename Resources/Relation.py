from http import HTTPStatus

from Models.Relation import Relation
from Resources.ApiResource import  ApiResource

class Relation(ApiResource):
    def post(self, id, targetParentId):
        relation = Relation(self.uri, self.user, self.password)
        relation.create(targetParentId,id);
        return {}, HTTPStatus.OK

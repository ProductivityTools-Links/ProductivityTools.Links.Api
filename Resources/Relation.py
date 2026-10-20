from http import HTTPStatus
from flask import request

from Models.Relation import Relation
from Resources.ApiResource import  ApiResource

class RelationResoure(ApiResource):
    def post(self):
        data = request.get_json(silent=True) or {}
        raw_id = data.get('id')
        raw_target_parent_id = data.get('targetParentId')

        if (
            raw_id is None
            or raw_target_parent_id is None
            or isinstance(raw_id, bool)
            or isinstance(raw_target_parent_id, bool)
        ):
            return {'message': 'Invalid id or targetParentId'}, HTTPStatus.BAD_REQUEST

        try:
            child_id = int(raw_id)
            target_parent_id = int(raw_target_parent_id)
        except (ValueError, TypeError):
            return {'message': 'id and targetParentId must be integers'}, HTTPStatus.BAD_REQUEST

        if child_id == target_parent_id:
            return {'message': 'Cannot move node into itself'}, HTTPStatus.BAD_REQUEST

        relation = Relation(self.uri, self.user, self.password)
        try:
            moved = relation.move(target_parent_id, child_id)
        finally:
            relation.close()

        if not moved:
            return {
                'message': 'Invalid move target (target missing, deleted, or descendant of source)'
            }, HTTPStatus.BAD_REQUEST

        return {}, HTTPStatus.OK

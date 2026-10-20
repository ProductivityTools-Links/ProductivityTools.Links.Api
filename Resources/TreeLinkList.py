
from Models.Links import Links
from Models.Relation import Relation
from flask import request, Response
import jsonpickle


from Resources.ApiResource import ApiResource


def _parse_include_archived():
    data = request.get_json(silent=True)
    if isinstance(data, dict) and "includeArchived" in data:
        val = data.get("includeArchived")
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().lower() in ("true", "1", "yes")
        return bool(val)
    arg = request.args.get("includeArchived")
    if arg is not None:
        return arg.strip().lower() in ("true", "1", "yes")
    return False


class TreeLinkListResource(ApiResource):
    def get(self, login):
        include_archived = _parse_include_archived()
        link = Links(self.uri, self.user, self.password)
        result = link.getTreeLinks(login, include_archived=include_archived)
        link.close()
        jsonresult = jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)

    def post(self, login):
        include_archived = _parse_include_archived()
        link = Links(self.uri, self.user, self.password)
        result = link.getTreeLinks(login, include_archived=include_archived)
        link.close()
        jsonresult = jsonpickle.encode(result, unpicklable=False)
        return Response(jsonresult, mimetype="text/json", direct_passthrough=True)



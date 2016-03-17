import json
from django.http import HttpResponse


def json_response(err, status):
    return HttpResponse(json.dumps(err, sort_keys=True), content_type="application/json; charset=UTF-8", status=status)

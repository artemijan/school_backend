from django.core import serializers
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from django.http import HttpResponse


@csrf_exempt
def reg(request):
    user = None
    logging.warning('request')
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
    if user is None:
        return serializers.serialize("json", None)
    else:
        return HttpResponse(json.dumps(serializers.serialize("json", [user, ])), content_type="application/json")

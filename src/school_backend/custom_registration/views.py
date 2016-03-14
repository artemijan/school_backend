from rest_api.serializers import UserSerializer
from rest_framework import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions
from django.http import HttpResponse
import json
from rest_framework import status


class RegistrationView(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        # do registration logic here
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps(serializer.data), content_type="application/json",
                                status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(json.dumps({"message": 'Data is not valid.'}), content_type="application/json",
                                status=status.HTTP_400_BAD_REQUEST)

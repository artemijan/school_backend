from custom_registration.models import ExtendedUser
from rest_framework import mixins, viewsets
from rest_api.serializers import UserSerializer
from rest_framework import permissions


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ExtendedUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

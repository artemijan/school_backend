from custom_registration.models import ExtendedUser
from rest_framework import serializers
from utils import json_response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            id: {
                'read_only': True
            }
        }

    def create(self, validated_data):
        try:
            user = ExtendedUser.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                last_name=validated_data['last_name'],
                first_name=validated_data['first_name']
            )
        except ExtendedUser.DoesNotExist, e:
            return json_response({"error": 201, "message": "Error while creating an instance User"}, 400)

        user.set_password(validated_data['password'])
        user.save()
        return user


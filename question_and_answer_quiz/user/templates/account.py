from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer
from user.models import UserModel


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]


class UserCallbackSerializer(serializers.Serializer):  # pylint: disable=W0223
    id = fields.IntegerField()  # pylint: disable=C0103
    email = fields.EmailField()
    username = fields.CharField(allow_blank=False)
    first_name = fields.CharField(allow_blank=False)
    last_name = fields.CharField(allow_blank=False)

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

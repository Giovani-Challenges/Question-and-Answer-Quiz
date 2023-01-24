from rest_framework.serializers import ModelSerializer
from django.forms import fields

from user.models import UserModel


class CreateUserSerializer(ModelSerializer):
    password = fields.RegexField(
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$*&@#])[0-9a-zA-Z$*&@#]{8,}$"
    )

    class Meta:
        model = UserModel
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]

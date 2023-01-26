from rest_framework import fields, serializers


class LoginSerializer(serializers.Serializer):  # pylint: disable=W0223
    password = fields.CharField()
    email = fields.EmailField()


class JwtTokensSerializer(serializers.Serializer):  # pylint: disable=W0223
    token = fields.CharField()
    refresh_token = fields.CharField()

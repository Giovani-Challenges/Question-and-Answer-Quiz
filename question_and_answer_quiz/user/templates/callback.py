from rest_framework import fields, serializers


class UserCallbackSerializer(serializers.Serializer): # pylint: disable=W0223
    id = fields.IntegerField() # pylint: disable=C0103
    email = fields.EmailField()
    username = fields.CharField(allow_blank=False)
    first_name = fields.CharField(allow_blank=False)
    last_name = fields.CharField(allow_blank=False)

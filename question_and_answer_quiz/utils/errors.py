from rest_framework.exceptions import APIException
from rest_framework import status


class UnprocessableEntity(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Unprocessable entity."
    default_code = "UNPROCESSABLE_ENTITY"


class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized."
    default_code = "UNAUTHORIZED"

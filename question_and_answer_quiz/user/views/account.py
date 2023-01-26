from typing import Literal

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from user.models import UserModel
from user.templates.account import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    UserCallbackSerializer,
)
from utils.permissions import IsAnyUser


class CreateUserViewSet(GenericViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, user_type: Literal["admin", "player"]):
        serializer = self.get_serializer(data=request.data)
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user_type == "admin":
            model = UserModel.objects.create_user(is_admin=True, **serializer.data)
        else:
            model = UserModel.objects.create_user(is_player=True, **serializer.data)
        callback = UserCallbackSerializer(data=model_to_dict(model))
        callback.is_valid(raise_exception=True)
        return Response(data=callback.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAnyUser]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserModel.objects.get(
                email=serializer.data["email"], id=request.user
            )
        except ObjectDoesNotExist:
            return Response(
                data={"message": "Invalid e-mail, use your own account e-mail"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if user.check_password(serializer.data["password"]):
            user.set_password(serializer.data["new_password"])
            user.save()
        else:
            return Response(
                data={"message": "Invalid Credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        callback = UserCallbackSerializer(data=model_to_dict(user))
        callback.is_valid(raise_exception=True)
        return Response(data=callback.data, status=status.HTTP_200_OK)

from typing import Literal
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from user.models import UserModel
from user.templates.callback import UserCallbackSerializer
from user.templates.create import CreateUserSerializer


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


class CreatePlayerView(GenericViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

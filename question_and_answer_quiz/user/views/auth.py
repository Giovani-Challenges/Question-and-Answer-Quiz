from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.jwt import JwtToken
from utils.decorators import inject
from user.models.user import UserModel
from user.templates.auth import (
    JwtTokensSerializer,
    LoginSerializer,
)
from jose.exceptions import ExpiredSignatureError
from django.core.exceptions import ObjectDoesNotExist


@inject(JwtToken)
class LoginView(APIView):
    jwttoken: JwtToken
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = UserModel.objects.get(email=serializer.data["email"])
        except ObjectDoesNotExist:
            user = None
        if user and user.check_password(serializer.data["password"]):
            callback = JwtTokensSerializer(
                data={
                    "token": self.jwttoken.encode(
                        token_type="TOKEN",
                        user_id=user.id,
                        permissions=user.permissions,
                    ),
                    "refresh_token": self.jwttoken.encode(
                        token_type="REFRESH_TOKEN",
                        user_id=user.id,
                        permissions=["REFRESH"],
                    ),
                }
            )
        else:
            return Response(
                data={"message": "Invalid Credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        callback.is_valid(raise_exception=True)
        return Response(
            data=callback.data,
            status=status.HTTP_200_OK,
        )


@inject(JwtToken)
class RefreshTokenView(APIView):
    jwttoken: JwtToken
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtTokensSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.jwttoken.decode(
            serializer.data["token"], options={"verify_exp": False}
        )
        try:
            refresh_token = self.jwttoken.decode(serializer.data["refresh_token"])
        except ExpiredSignatureError:
            return Response(
                data={"message": "Expired 'refresh_token', please do the login again"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if token.get("user") != refresh_token.get("user"):
            return Response(
                data={"message": "'token' does not match with 'refresh_token'"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if refresh_token.get("permissions") == ["REFRESH"]:
            callback = JwtTokensSerializer(
                data={
                    "token": self.jwttoken.encode(
                        token_type="TOKEN",
                        user_id=token.get("user"),
                        permissions=token.get("permissions"),
                    ),
                    "refresh_token": self.jwttoken.encode(
                        token_type="REFRESH_TOKEN",
                        user_id=refresh_token.get("user"),
                        permissions=["REFRESH"],
                    ),
                }
            )
        else:
            return Response(
                data={"message": "'refresh_token' is not a valid refresh token"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        callback.is_valid(raise_exception=True)
        return Response(data=callback.data, status=status.HTTP_200_OK)

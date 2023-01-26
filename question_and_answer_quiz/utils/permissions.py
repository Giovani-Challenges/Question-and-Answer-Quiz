from typing import List, Optional, Tuple

from jose.exceptions import ExpiredSignatureError, JWTError
from rest_framework.permissions import BasePermission
from user.views.errors import Unauthorized, UnprocessableEntity
from utils.decorators import inject
from utils.jwt import JwtToken


@inject(JwtToken)
class BaseBearer(BasePermission):
    jwttoken: JwtToken

    def get_authorization_content(self, authorization: str) -> Tuple[str, str]:
        _type, token, *_ = authorization.split(" ")
        return _type, token

    def get_authorization_from_header(self, header) -> Optional[dict]:
        return header.get("Authorization")

    def contain_permission(self, permissions: List[str], payload: dict):
        payload_permissions = payload.get("permissions", [])
        for permission in payload_permissions:
            if not permission in permissions:
                return False
        return True

    def is_bearer(self, _type: str):
        return _type == "Bearer"

    def has_permission(self, request, view, **kwargs) -> bool:
        authorization = self.get_authorization_from_header(request.headers)
        if not authorization:
            raise UnprocessableEntity(
                detail="You must provide a Authorization header with Bearer token"
            )
        _type, token = self.get_authorization_content(authorization)
        if not self.is_bearer(_type):
            raise UnprocessableEntity(
                detail="You must provide a Authorization header with Bearer token"
            )
        try:
            payload = self.jwttoken.decode(token)
        except ExpiredSignatureError:
            raise Unauthorized(  # pylint: disable=W0707
                detail="Expired token. Please refresh your token or make the login again"
            )
        except JWTError:
            raise Unauthorized(  # pylint: disable=W0707
                detail="Invalid token. Please do the login in our api or register your account"
            )
        if not self.contain_permission(
            permissions=kwargs.get("permissions", []), payload=payload
        ):
            raise Unauthorized(detail="You don't have permission to use this endpoint")
        request.user = payload.get("user")
        return True


class IsAdm(BaseBearer):
    def has_permission(self, request, view, **kwargs) -> bool:
        return super().has_permission(request, view, permissions=["ADM"])


class IsPlayer(BaseBearer):
    def has_permission(self, request, view, **kwargs) -> bool:
        return super().has_permission(request, view, permissions=["PLAYER"])


class IsAnyUser(BaseBearer):
    def has_permission(self, request, view, **kwargs) -> bool:
        return super().has_permission(request, view, permissions=["PLAYER", "ADM"])

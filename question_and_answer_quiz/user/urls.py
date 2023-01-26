from django.urls import path, re_path

from user.views.auth import LoginView, RefreshTokenView
from user.views.account import CreateUserViewSet

urlpatterns = [
    re_path(
        r"account/create/(?P<user_type>admin|player+)/$",
        CreateUserViewSet.as_view({"post": "create"}),
        name="Create admin user",
    ),
    path("auth/login/", LoginView.as_view(), name="User Login"),
    path(
        "auth/refresh/",
        RefreshTokenView.as_view(),
        name="Refresh token from user",
    ),
]

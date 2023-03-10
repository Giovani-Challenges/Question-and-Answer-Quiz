from django.urls import path, re_path
from user.views.account import ChangePasswordView, CreateUserViewSet
from user.views.auth import LoginView, RefreshTokenView

urlpatterns = [
    re_path(
        r"account/create/(?P<user_type>admin|player+)/$",
        CreateUserViewSet.as_view({"post": "create"}),
        name="Create admin user",
    ),
    path(
        "account/change-password/",
        ChangePasswordView.as_view(),
        name="Change user password",
    ),
    path("auth/login/", LoginView.as_view(), name="User Login"),
    path(
        "auth/refresh/",
        RefreshTokenView.as_view(),
        name="Refresh token from user",
    ),
]

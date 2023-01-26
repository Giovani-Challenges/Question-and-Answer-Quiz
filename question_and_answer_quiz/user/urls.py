from django.urls import path

from user.views.auth import LoginView, RefreshTokenView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="User Login"),
    path(
        "auth/refresh/",
        RefreshTokenView.as_view(),
        name="Refresh token from user",
    ),
]

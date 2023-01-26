from django.urls import re_path

from user.views.account import CreateUserViewSet

urlpatterns = [
    re_path(
        r"account/create/(?P<user_type>admin|player+)/$",
        CreateUserViewSet.as_view({"post": "create"}),
        name="Create admin user",
    )
]

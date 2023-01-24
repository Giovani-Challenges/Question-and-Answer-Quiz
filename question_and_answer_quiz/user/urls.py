from django.urls import re_path

from question_and_answer_quiz.user.views.create import CreateUserViewSet

urlpatterns = [
    re_path(
        r"create/(?P<user_type>admin|player+)/$",
        CreateUserViewSet.as_view({"post": "create"}),
        name="Create admin user",
    )
]

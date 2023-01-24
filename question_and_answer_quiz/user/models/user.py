from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        username: str,
        password: str,
        is_admin: bool = False,
        is_player: bool = False,
        **kwargs
    ) -> models.Model:
        if not email:
            raise ValueError("E-mail must be set")
        if not username:
            raise ValueError("Username must be set")
        if not password:
            raise ValueError("Password must be set")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            created_date=datetime.now(),
            is_admin=is_admin,
            is_player=is_player,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class UserModel(AbstractBaseUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=75)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(null=True)
    is_admin = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # pylint: disable=C0103
    REQUIRED_FIELDS = ["email", "username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "User"
        app_label = "user"

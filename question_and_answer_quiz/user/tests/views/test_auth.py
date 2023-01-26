from datetime import datetime, timedelta
import os
from django.test import TestCase
from jose import jwt
from jose.constants import ALGORITHMS
import pytest
from user.models.user import UserModel


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.player = UserModel.objects.create_user(
            email="player-test@gmail.com",
            username="player-user",
            password="123abc",
            is_player=True,
        )
        self.admin = UserModel.objects.create_user(
            email="admin-test@gmail.com",
            username="admin-user",
            password="123abc",
            is_admin=True,
        )
        return super().setUp()

    def test_should_login_with_invalid_credentials(self):
        response = self.client.post(
            "/user/auth/login/",
            data={"password": "123", "email": "test@tested.com"},
            content_type="application/json",
        )

        assert response.status_code == 401
        assert response.json() == {"message": "Invalid Credentials"}

    @pytest.mark.freeze_time("2017-05-21")
    def test_shoul_login_as_admin(self):
        response = self.client.post(
            "/user/auth/login/",
            data={"password": "123abc", "email": "admin-test@gmail.com"},
            content_type="application/json",
        )

        json = response.json()
        token = jwt.decode(
            token=json.get("token"),
            key=None,
            algorithms=ALGORITHMS.HS512,
            options={"verify_signature": False},
        )
        refresh_token = jwt.decode(
            token=json.get("refresh_token"),
            key=None,
            algorithms=ALGORITHMS.HS512,
            options={"verify_signature": False},
        )

        assert response.status_code == 200
        assert token == {"permissions": ["ADM"], "user": 2, "exp": 1495346400.0}
        assert refresh_token == {
            "permissions": ["REFRESH"],
            "user": 2,
            "exp": 1495368000.0,
        }

    @pytest.mark.freeze_time("2017-05-21")
    def test_shoul_login_as_player(self):
        response = self.client.post(
            "/user/auth/login/",
            data={"password": "123abc", "email": "player-test@gmail.com"},
            content_type="application/json",
        )

        json = response.json()
        token = jwt.decode(
            token=json.get("token"),
            key=None,
            algorithms=ALGORITHMS.HS512,
            options={"verify_signature": False},
        )
        refresh_token = jwt.decode(
            token=json.get("refresh_token"),
            key=None,
            algorithms=ALGORITHMS.HS512,
            options={"verify_signature": False},
        )

        assert response.status_code == 200
        assert token == {"permissions": ["PLAYER"], "user": 1, "exp": 1495346400.0}
        assert refresh_token == {
            "permissions": ["REFRESH"],
            "user": 1,
            "exp": 1495368000.0,
        }


class TestRefreshToken(TestCase):
    @pytest.mark.freeze_time("2017-05-21")
    def test_should_do_not_refresh_token_when_exp_field_has_been_expired_from_refresh_token(
        self,
    ):
        token = jwt.encode(
            claims={
                "permissions": ["PLAYER"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() - timedelta(hours=3)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        refresh_token = jwt.encode(
            claims={
                "permissions": ["REFRESH"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() - timedelta(hours=6)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        response = self.client.post(
            "/user/auth/refresh/",
            data={"token": token, "refresh_token": refresh_token},
            content_type="application/json",
        )

        assert response.status_code == 422
        assert response.json() == {
            "message": "Expired 'refresh_token', please do the login again"
        }

    @pytest.mark.freeze_time("2017-05-21")
    def test_should_do_not_refresh_token_when_contain_different_user_id_in_token_and_refresh_token(
        self,
    ):
        token = jwt.encode(
            claims={
                "permissions": ["PLAYER"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() - timedelta(hours=3)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        refresh_token = jwt.encode(
            claims={
                "permissions": ["REFRESH"],
                "user": 2,
                "exp": datetime.timestamp(datetime.now() + timedelta(hours=6)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        response = self.client.post(
            "/user/auth/refresh/",
            data={"token": token, "refresh_token": refresh_token},
            content_type="application/json",
        )

        assert response.status_code == 422
        assert response.json() == {
            "message": "'token' does not match with 'refresh_token'"
        }

    @pytest.mark.freeze_time("2017-05-21")
    def test_should_refresh_token_field_does_not_contain_refresh_permission(self):
        token = jwt.encode(
            claims={
                "permissions": ["PLAYER"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() - timedelta(hours=3)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        refresh_token = jwt.encode(
            claims={
                "permissions": ["PLAYER"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() + timedelta(hours=6)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        response = self.client.post(
            "/user/auth/refresh/",
            data={"token": token, "refresh_token": refresh_token},
            content_type="application/json",
        )

        assert response.status_code == 422
        assert response.json() == {
            "message": "'refresh_token' is not a valid refresh token"
        }

    @pytest.mark.freeze_time("2017-05-21")
    def test_should_refresh_token(self):
        token = jwt.encode(
            claims={
                "permissions": ["PLAYER"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() - timedelta(hours=3)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        refresh_token = jwt.encode(
            claims={
                "permissions": ["REFRESH"],
                "user": 1,
                "exp": datetime.timestamp(datetime.now() + timedelta(hours=6)),
            },
            key=os.environ["JWT_SECRET_KEY"],
            algorithm=ALGORITHMS.HS512,
        )
        response = self.client.post(
            "/user/auth/refresh/",
            data={"token": token, "refresh_token": refresh_token},
            content_type="application/json",
        )
        json = response.json()
        json_token = jwt.decode(
            token=json.get("token"),
            key=os.environ["JWT_SECRET_KEY"],
            algorithms=ALGORITHMS.HS512,
        )
        json_refresh_token = jwt.decode(
            token=json.get("refresh_token"),
            key=os.environ["JWT_SECRET_KEY"],
            algorithms=ALGORITHMS.HS512,
        )

        assert response.status_code == 200
        assert json_token == {"permissions": ["PLAYER"], "user": 1, "exp": 1495346400.0}
        assert json_refresh_token == {
            "permissions": ["REFRESH"],
            "user": 1,
            "exp": 1495368000.0,
        }

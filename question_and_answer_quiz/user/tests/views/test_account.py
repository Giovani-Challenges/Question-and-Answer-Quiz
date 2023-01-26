from django.test import TestCase
from utils.jwt import JwtToken
from user.models.user import UserModel


class TestCreateAdminView(TestCase):
    def test_should_create_admin_user(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            body,
            {
                "id": 1,
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
            },
        )

    def test_should_user_have_invalid_email(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"email": ["Enter a valid email address."]})

    def test_should_user_have_blank_username(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django@test.com",
                "username": "",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"username": ["This field may not be blank."]})

    def test_should_user_have_blank_first_name(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"first_name": ["This field may not be blank."]})

    def test_should_user_have_blank_last_name(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"last_name": ["This field may not be blank."]})

    def test_should_user_have_blank_password(self):
        response = self.client.post(
            "/user/account/create/admin/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"password": ["This field may not be blank."]})


class TestCreatPlayerView(TestCase):
    def test_should_create_player_user(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-player-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            body,
            {
                "id": 1,
                "email": "test-player-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
            },
        )

    def test_should_user_have_invalid_email(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-admin-django.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"email": ["Enter a valid email address."]})

    def test_should_user_have_blank_username(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-admin-django@test.com",
                "username": "",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"username": ["This field may not be blank."]})

    def test_should_user_have_blank_first_name(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "",
                "last_name": "from giovani",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"first_name": ["This field may not be blank."]})

    def test_should_user_have_blank_last_name(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "",
                "password": "123",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"last_name": ["This field may not be blank."]})

    def test_should_user_have_blank_password(self):
        response = self.client.post(
            "/user/account/create/player/",
            data={
                "email": "test-admin-django@test.com",
                "username": "testing",
                "first_name": "tested",
                "last_name": "from giovani",
                "password": "",
            },
            content_type="application/json",
        )

        body = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {"password": ["This field may not be blank."]})


class TestChangePassword(TestCase):
    def setUp(self) -> None:
        self.pwd = "abc123"
        self.player = UserModel.objects.create_user(
            email="player@test.com",
            username="testing-01",
            password=self.pwd,
            is_player=True,
            first_name="CS",
            last_name="Player",
        )
        self.adm = UserModel.objects.create_user(
            email="adm@test.com",
            username="testing-02",
            password=self.pwd,
            is_admin=True,
            first_name="adm",
            last_name="last name",
        )
        jwt = JwtToken()
        self.adm = {
            "instance": self.adm,
            "token": jwt.encode(
                user_id=self.adm.id,
                token_type="TOKEN",
                permissions=self.adm.permissions,
            ),
            "refresh-token": jwt.encode(
                user_id=self.adm.id,
                token_type="REFRESH_TOKEN",
                permissions=["REFRESH_TOKEN"],
            ),
        }
        self.player = {
            "instance": self.player,
            "token": jwt.encode(
                user_id=self.player.id,
                token_type="TOKEN",
                permissions=self.player.permissions,
            ),
            "refresh-token": jwt.encode(
                user_id=self.player.id,
                token_type="REFRESH_TOKEN",
                permissions=["REFRESH_TOKEN"],
            ),
        }
        return super().setUp()

    def test_should_return_unprocessablee_entity_when_you_dont_send_a_token(self):
        response = self.client.post(
            "/user/account/change-password/",
            data={
                "email": "player@test.com",
                "password": self.pwd,
                "new_password": "abc1234",
            },
            content_type="application/json",
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "You must provide a Authorization header with Bearer token"
        }

    def test_should_return_unhautorized_when_try_to_change_a_password_with_invalid_email(
        self,
    ):
        response = self.client.post(
            "/user/account/change-password/",
            data={
                "email": self.player["instance"].email,
                "password": self.pwd,
                "new_password": "abc1234",
            },
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.adm['token']}"},
        )

        assert response.status_code == 401
        assert response.json() == {
            "message": "Invalid e-mail, use your own account e-mail"
        }

    def test_should_return_unhautorized_when_try_to_change_a_password_with_invalid_password_confirmation(  # pylint: disable=C0301
        self,
    ):
        response = self.client.post(
            "/user/account/change-password/",
            data={
                "email": self.player["instance"].email,
                "password": "invalid",
                "new_password": "abc1234",
            },
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.player['token']}"},
        )

        assert response.status_code == 401
        assert response.json() == {"message": "Invalid Credentials"}

    def test_should_change_password_from_player(self):
        response = self.client.post(
            "/user/account/change-password/",
            data={
                "email": self.player["instance"].email,
                "password": self.pwd,
                "new_password": "newPWD",
            },
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.player['token']}"},
        )
        user = UserModel.objects.get(id=1)

        assert response.status_code == 200
        assert user.password != self.player["instance"].password
        assert user.check_password("newPWD")
        assert response.json() == {
            "id": 1,
            "email": "player@test.com",
            "username": "testing-01",
            "first_name": "CS",
            "last_name": "Player",
        }

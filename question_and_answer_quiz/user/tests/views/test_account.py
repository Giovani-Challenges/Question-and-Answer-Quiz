from django.test import TestCase


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

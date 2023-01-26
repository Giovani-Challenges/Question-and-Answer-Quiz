from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from user.models.user import UserModel


class TestUserModel(TestCase):
    def test_should_insert_one_user(self):
        instance = UserModel.objects.create(
            email="test@test.com",
            username="testing",
            first_name="test",
            last_name="testing tested",
            created_date=datetime.strptime("09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"),
        )

        self.assertEqual(instance.id, 1)
        self.assertEqual(instance.email, "test@test.com")
        self.assertEqual(instance.username, "testing")
        self.assertEqual(instance.first_name, "test")
        self.assertEqual(instance.last_name, "testing tested")
        self.assertEqual(
            instance.created_date,
            datetime.strptime("09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"),
        )
        self.assertEqual(instance.updated_date, None)

    def test_should_raise_integrity_error_when_insert_more_than_one_user_with_the_same_email(
        self,
    ):
        instance = UserModel.objects.create(
            email="test@test.com",
            username="testing-01",
            first_name="test",
            last_name="testing tested",
            created_date=datetime.strptime("09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"),
        )
        with self.assertRaises(IntegrityError):
            UserModel.objects.create(
                email=instance.email,
                username="testing-02",
                first_name="test",
                last_name="testing tested",
                created_date=datetime.strptime(
                    "09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"
                ),
            )

    def test_should_raise_integrity_error_when_insert_more_than_one_user_with_the_same_username(
        self,
    ):
        instance = UserModel.objects.create(
            email="test-01@test.com",
            username="testing-01",
            first_name="test",
            last_name="testing tested",
            created_date=datetime.strptime("09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"),
        )
        with self.assertRaises(IntegrityError):
            UserModel.objects.create(
                email="test-02@test.com",
                username=instance.username,
                first_name="test",
                last_name="testing tested",
                created_date=datetime.strptime(
                    "09/19/22 13:55:26", "%m/%d/%y %H:%M:%S"
                ),
            )

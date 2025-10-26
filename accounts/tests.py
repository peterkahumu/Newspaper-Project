import uuid
from datetime import date
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UserManagersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        dob = date(2000, 8, 20)
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(
            username="test_user",
            email="test_user@test.com",
            password="testuserpassword1234",
            date_of_birth=dob,
        )
        cls.super_user = cls.User.objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin1234"
        )

    def test_normal_user(self):
        """Test the properties of a normal user"""
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.email, "test_user@test.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_super_user(self):
        """Test the properties of a superuser."""
        self.assertEqual(self.super_user.username, "admin")
        self.assertEqual(self.super_user.email, "admin@admin.com")
        self.assertTrue(self.super_user.is_active)
        self.assertTrue(self.super_user.is_staff)
        self.assertTrue(self.super_user.is_superuser)

    def test_password_hashed(self):
        """Make sure that the user's password is hashed."""
        self.assertNotEqual(self.user.password, "testuserpassword1234")
        self.assertNotEqual(self.super_user.password, "admin1234")

    def test_user_id_is_uuid(self):
        """Make sure that the user id is generated as expected."""
        self.assertIsNotNone(self.user.user_id)
        self.assertIsInstance(self.user.user_id, uuid.UUID)
        self.assertIsInstance(self.super_user.user_id, uuid.UUID)

    def test_age_property(self):
        """Make sure that the age is calculated properly."""
        today = timezone.now().date()
        dob = self.user.date_of_birth
        expected_age = (
            today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        )

        self.assertIsNotNone(self.user.date_of_birth)
        self.assertEqual(self.user.age, expected_age)

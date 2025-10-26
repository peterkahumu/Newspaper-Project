import uuid
from datetime import date, datetime
from unittest.mock import patch
from django.utils import timezone
from django.urls import reverse
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

    def test_is_birthday(self):
        """Test to make sure birthday works well."""
        self.user.date_of_birth = timezone.now().date()
        self.user.save()
        self.assertTrue(self.user.is_birthday)

    def test_leap_year_birthday(self):
        self.user.date_of_birth = date(2004, 2, 29)
        self.user.save()
        today = date(2025, 2, 28)

        with patch(
            "django.utils.timezone.now",
            return_value=timezone.make_aware(
                datetime.combine(today, datetime.min.time())
            ),
        ):
            self.assertTrue(self.user.is_birthday)


class RegisterUsersTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.url = self.client.get("/accounts/register/")
        self.url_name = self.client.get(reverse("register"))
        self.user_register = self.client.post(
            reverse("register"),
            {
                "first_name": "test",
                "last_name": "testlast",
                "username": "testusername",
                "email": "test@test.com",
                "password1": "Testuser12345",
                "password2": "Testuser12345",
            },
        )

    def test_register_url(self):
        """Test urls behave as expected."""
        self.assertEqual(self.url.status_code, 200)
        self.assertEqual(self.url_name.status_code, 200)

        self.assertTemplateUsed(self.url, "registration/register.html")
        self.assertTemplateUsed(self.url_name, "registration/register.html")

        self.assertRedirects(self.user_register, reverse("login"))

    def test_register_process(self):
        """Test user registration form."""
        user = self.User.objects.get(username="testusername")

        self.assertEqual(self.user_register.status_code, 302)
        self.assertEqual(self.User.objects.all().count(), 1)
        self.assertEqual(user.username, "testusername")
        self.assertEqual(user.email, "test@test.com")

    def test_register_invalid_user_password_mismatcth(self):
        """Ensure invalid data raises an error."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "baduser",
                "first_name": "baduser",
                "last_name": "baduser",
                "email": "baduser@test.com",
                "password1": "Baduser1234",
                "password2": "baduser1234",
            },
        )

        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertIn("The two password fields didn’t match.", form.errors["password2"])

    def test_register_missing_fields(self):
        response = self.client.post(
            reverse("register"),
            {
                "password1": "password",
            },
        )

        form = response.context["form"]

        self.assertIn("This field is required.", form.errors["username"])
        self.assertIn("This field is required.", form.errors["password2"])

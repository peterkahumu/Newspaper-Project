import uuid
from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    """Create a Custom User with additional fields."""

    user_id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    date_of_birth = models.DateField(null=True, blank=True)

    @property
    def age(self):
        today = timezone.now().date()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @property
    def is_birthday(self):
        if not self.date_of_birth:
            return False  # Gracefully handle missing Date of Birth field.
        today = timezone.now().date()
        try:
            this_year_birthday = self.date_of_birth.replace(year=today.year)
        except ValueError:
            # Handles Feb 29 on non-leap years
            this_year_birthday = self.date_of_birth.replace(year=today.year, day=28)
        return this_year_birthday == today

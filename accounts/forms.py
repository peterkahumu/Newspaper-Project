from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Create a Custom user registration form to capture additional fields."""

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("date_of_birth",)


class CustomUserChangeForm(UserChangeForm):
    """Create a custom form to change the user."""

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

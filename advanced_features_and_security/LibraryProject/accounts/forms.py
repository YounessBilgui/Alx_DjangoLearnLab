from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form that includes additional fields."""
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Optional: Your date of birth"
    )
    profile_photo = forms.ImageField(
        required=False,
        help_text="Optional: Upload a profile photo"
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field required
        self.fields['email'].required = True
        # Add help text for existing fields
        self.fields['email'].help_text = "Required: Enter a valid email address"
        self.fields['first_name'].help_text = "Optional: Your first name"
        self.fields['last_name'].help_text = "Optional: Your last name"


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form for admin interface."""
    
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }

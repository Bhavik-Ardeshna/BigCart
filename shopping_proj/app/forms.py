from . import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['ratings','review']


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

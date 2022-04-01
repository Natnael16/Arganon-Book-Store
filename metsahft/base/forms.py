from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.save()
        return user


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = "__all__"


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["phone"]

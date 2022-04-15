from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class BookForm(ModelForm):
    # checkbox =forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox'}))
    class Meta:
        model = Book
        fields = '__all__'
        # exclude = ['image_front_ref' , 'image_back_ref']
class PackageForm(ModelForm):

    class Meta:
        model = Packages
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    አስተያየት = forms.CharField(widget=forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder':' አስተያየቶን ይፃፉ',
        'rows' : "4",
        'cols':'50'
    }))
    class Meta:
        model = Review
        fields = ['አስተያየት']
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["phone"]
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.save()
        return user

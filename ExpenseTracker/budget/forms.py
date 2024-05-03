from django import forms
from django.contrib.auth.models import User

class UpdateUserForm(forms.ModelForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username']
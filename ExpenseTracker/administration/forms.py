from django import forms
from .models import User

class AddUserForm(forms.ModelForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  password = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
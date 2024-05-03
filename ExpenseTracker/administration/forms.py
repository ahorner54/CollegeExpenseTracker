from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddUserForm(UserCreationForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))  
  password1 = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Password1"}))
  password2 = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Password2"}))
 
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']



class UpdateUserForm(forms.ModelForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username']

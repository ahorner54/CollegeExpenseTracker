from django import forms
from django.contrib.auth.models import User

class AddUserForm(forms.ModelForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Password"}))
  

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password', 'groups']

  def __init__(self, *args, **kwargs):
    super(AddUserForm, self).__init__(*args, **kwargs)

    self.fields["first_name"].widget.attrs["class"] = "form-control"
    self.fields["first_name"].widget.attrs['placeholder'] = "First Name"
    self.fields["first_name"].label = ""

    self.fields["groups"].widget.attrs["class"] = "form-control"
    self.fields["groups"].widget.attrs['placeholder'] = "First Name"
    self.fields["groups"].label = ""


class AddAdminForm(forms.ModelForm):
  email = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  first_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
  last_name = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
  username = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(required=True, label="", widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Password"}))
  

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password', 'groups', 'is_staff']
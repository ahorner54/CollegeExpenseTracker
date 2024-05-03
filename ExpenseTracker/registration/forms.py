from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control w-25','type':'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs['placeholder'] = "User Name"
        self.fields["username"].label = ""

        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs['placeholder'] = "First Name"
        self.fields["first_name"].label = ""

        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs['placeholder'] = "Last Name"
        self.fields["last_name"].label = ""

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs['placeholder'] = "Email Address"
        self.fields["email"].label = ""

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs['placeholder'] = "Password"
        self.fields["password1"].label = ""

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs['placeholder'] = "Password"
        self.fields["password2"].label = ""
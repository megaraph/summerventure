from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=60,
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=60,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password "}),
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        max_length=60,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password again"}),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if User.objects.filter(username=username).first() is not None:
            self.add_error("username", "Account with that username already exists")

        try:
            validate_password(
                password=password,
            )
        except forms.ValidationError as e:
            self.add_error("password", e)

        if not password == password_confirm:
            self.add_error("password_confirm", "Passwords do not match. Try again.")

        return cleaned_data

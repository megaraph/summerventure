from tkinter import W
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
        label="Password",
        max_length=60,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password again"}),
    )

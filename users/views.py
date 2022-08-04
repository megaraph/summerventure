from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import RegistrationForm


def login_view(request):
    context = {"message": "sup"}
    return render(request, "users/login.html", context=context)


def signup_view(request):
    form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context=context)

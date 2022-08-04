from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import RegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    context = {"message": "sup"}
    return render(request, "users/login.html", context=context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    form = RegistrationForm(data=request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        return redirect("signup")

    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("login")

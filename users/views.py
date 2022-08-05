from pathlib import Path
from venv import create

from django.core.files import File
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .forms import RegistrationForm, LoginForm
from .utils import get_avatar, create_avatar_file, delete_avatar_file
from .models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    form = LoginForm(data=request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        login(request, user)
        return redirect("challenges:explore")

    context = {
        "form": form,
    }
    return render(request, "users/login.html", context=context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    form = RegistrationForm(data=request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        avatar_success, avatar, new_file_name = get_avatar(username)

        print(avatar_success, avatar)

        if not avatar_success:
            messages.add_message(
                request,
                messages.ERROR,
                "There was an error signing you up. Try again later.",
            )
            return redirect("signup")

        new_user = User.objects.create_user(username=username, password=password)

        new_avatar_file = create_avatar_file(new_file_name, avatar)
        Profile.objects.create(
            user=new_user,
            avatar=File(file=open(new_avatar_file, "rb"), name=new_file_name),
        )
        delete_avatar_file(new_avatar_file)

        login(request, new_user)
        return redirect("challenges:explore")

    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("login")

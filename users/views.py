import tempfile

from django.core.files import File
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm
from .utils import get_avatar
from .models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    context = {"message": "sup"}
    return render(request, "users/login.html", context=context)


def signup_view(request):
    # if request.user.is_authenticated:
    #     return redirect("challenges:explore")

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

        with tempfile.NamedTemporaryFile(delete=True) as temp_img:
            temp_img.write(avatar)

            new_profile = Profile.objects.create(user=new_user)
            new_profile.avatar.save(new_file_name, File(temp_img))

        return redirect("signup")

    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("login")

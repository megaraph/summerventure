from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import Profile


@login_required
def home(request):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()

    context = {
        "current_user": current_user,
        "user_profile": user_profile,
    }

    return render(request, "challenges/home.html", context=context)

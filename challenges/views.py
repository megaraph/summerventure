from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import Profile
from .models import Challenge


@login_required
def home(request):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenges = Challenge.objects.all()

    context = {
        "current_user": current_user,
        "user_profile": user_profile,
        "challenges": challenges,
    }

    return render(request, "challenges/home.html", context=context)


@login_required
def create_challenge_post_view(request):
    return render(request, "challenges/post-create.html", context={})

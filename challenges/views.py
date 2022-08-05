from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import Profile
from .models import Challenge, Post, PostUpvote

from .utils import get_featured_challenges


@login_required
def home(request):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenges = Challenge.objects.all()
    featured_challenges = get_featured_challenges(challenges, 4)

    context = {
        "current_user": current_user,
        "user_profile": user_profile,
        "challenges": challenges,
        "featured_challenges": featured_challenges,
    }

    return render(request, "challenges/home.html", context=context)


@login_required
def challenge_detail_view(request, id):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenge = get_object_or_404(Challenge, pk=id)
    posts = challenge.get_all_posts()
    context = {
        "current_user": current_user,
        "user_profile": user_profile,
        "challenge": challenge,
        "posts": posts,
    }
    return render(request, "challenges/detail.html", context=context)


@login_required
def challenge_post_upvote(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        post.upvote_post(request.user)
        context = {
            "post": post,
        }

    return render(request, "challenges/partials/post-meta-info.html", context=context)


@login_required
def create_challenge_post_view(request):
    return render(request, "challenges/post-create.html", context={})

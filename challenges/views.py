from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from users.models import Profile
from .models import Challenge, Post, Comment

from .utils import get_featured_challenges, get_random_challenge


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
def random_challenge_view(request):
    challenge = get_random_challenge(Challenge.objects.all())
    return redirect(challenge.get_absolute_url())


@login_required
def post_detail_view(request, chal_id, id):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenge = get_object_or_404(Challenge, pk=chal_id)
    post = get_object_or_404(Post, pk=id)
    comments = post.get_all_comments()
    context = {
        "post": post,
        "current_user": current_user,
        "user_profile": user_profile,
        "challenge": challenge,
        "comments": comments,
    }
    return render(request, "challenges/post-detail.html", context=context)


@login_required
def create_challenge_post_view(request):
    return render(request, "challenges/post-create.html", context={})


@login_required
def comment_vote(request, id, action):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=id)
        comment.vote_comment(request.user, action)

        context = {
            "comment": comment,
        }

    return render(
        request, "challenges/partials/comment-meta-info.html", context=context
    )

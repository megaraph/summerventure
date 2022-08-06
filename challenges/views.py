from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from users.models import Profile
from .models import Challenge, Post, Comment, Attempt

from .utils import get_featured_challenges, get_random_challenge
from .forms import CommentCreationForm, PostCreationForm


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

    attempt = Attempt.objects.filter(
        user=request.user, challenge=challenge, status="p"
    ).first()

    if attempt:
        if attempt.expected_end_timestamp <= timezone.now():
            return redirect(challenge.get_challenge_finish_url("failed"))

    context = {
        "current_user": current_user,
        "user_profile": user_profile,
        "challenge": challenge,
        "posts": posts,
        "attempt": attempt,
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
def accept_challenge(request, id):
    challenge = get_object_or_404(Challenge, pk=id)
    attempt = Attempt.objects.filter(
        user=request.user, challenge=challenge, status="p"
    ).first()

    if attempt is not None:
        return redirect(challenge.get_absolute_url())

    Attempt.objects.create(user=request.user, challenge=challenge, status="p")
    return redirect(challenge.get_absolute_url())


@login_required
def finish_challenge(request, id, action):
    challenge = get_object_or_404(Challenge, pk=id)
    attempt = Attempt.objects.filter(
        user=request.user, challenge=challenge, status="p"
    ).first()
    if attempt is None:
        return redirect(challenge.get_absolute_url())

    status = {
        "done": "d",
        "failed": "f",
    }

    attempt.status = status.get(action)
    attempt.actual_end_timestamp = timezone.now()
    attempt.save()
    return redirect(challenge.get_absolute_url())


@login_required
def post_detail_view(request, chal_id, id):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenge = get_object_or_404(Challenge, pk=chal_id)
    post = get_object_or_404(Post, pk=id)
    comments = post.get_all_comments()

    form = CommentCreationForm(data=request.POST or None)

    if form.is_valid():
        message = form.cleaned_data.get("message")
        new_comment = Comment.objects.create(
            user=current_user, post=post, challenge=challenge, message=message
        )
        return redirect(new_comment.get_absolute_url())

    context = {
        "post": post,
        "current_user": current_user,
        "user_profile": user_profile,
        "challenge": challenge,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "challenges/post-detail.html", context=context)


@login_required
def create_challenge_post_view(request, chal_id):
    challenge = get_object_or_404(Challenge, pk=chal_id)
    current_attempt = Attempt.objects.filter(
        user=request.user, challenge=challenge, status="p"
    ).first()

    if current_attempt is None:
        return redirect(challenge.get_absolute_url())

    if current_attempt.expected_end_timestamp <= timezone.now():
        return redirect(challenge.get_challenge_finish_url("failed"))

    form = PostCreationForm()
    print(form.data)

    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.challenge = challenge
            new_post.save()

            return redirect(challenge.get_challenge_finish_url("done"))

    context = {
        "challenge": challenge,
        "form": form,
    }
    return render(request, "challenges/post-create.html", context=context)


@login_required
def comment_detail_view(request, chal_id, post_id, id):
    current_user = request.user
    user_profile = Profile.objects.filter(user=current_user).first()
    challenge = get_object_or_404(Challenge, pk=chal_id)
    post = get_object_or_404(Post, pk=post_id)
    parent_comment = get_object_or_404(Comment, pk=id)

    comments = parent_comment.get_all_replies()

    form = CommentCreationForm(data=request.POST or None)

    if form.is_valid():
        message = form.cleaned_data.get("message")
        new_comment = Comment.objects.create(
            user=current_user,
            post=post,
            challenge=challenge,
            parent_comment=parent_comment,
            message=message,
        )
        return redirect(new_comment.get_absolute_url())

    context = {
        "current_user": current_user,
        "user_profile": user_profile,
        "challenge": challenge,
        "post": post,
        "comment": parent_comment,
        "reply_form": form,
        "comments": comments,
    }
    return render(request, "challenges/comment-detail.html", context=context)


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

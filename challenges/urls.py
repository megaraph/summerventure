from django.urls import path

from . import views

app_name = "challenges"
urlpatterns = [
    path("explore/", views.home, name="explore"),
    path("challenge/<int:id>/", views.challenge_detail_view, name="detail"),
    path("challenge/random/", views.random_challenge_view, name="random"),
    path(
        "challenge/<int:chal_id>/post/<int:id>/",
        views.post_detail_view,
        name="post_detail",
    ),
    path("post/create/", views.create_challenge_post_view, name="create_post"),
    path("post/<int:id>/upvote/", views.challenge_post_upvote, name="post_upvote"),
    path(
        "comment/<int:id>/vote/<str:action>/",
        views.comment_vote,
        name="comment_vote",
    ),
]

from django.urls import path

from . import views

app_name = "challenges"
urlpatterns = [
    path("explore/", views.home, name="explore"),
    path("challenge/<int:id>/", views.challenge_detail_view, name="detail"),
    path("post/create/", views.create_challenge_post_view, name="create_post"),
    path("post/<int:id>/upvote/", views.challenge_post_upvote, name="post_upvote"),
]

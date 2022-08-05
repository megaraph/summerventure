from django.urls import path

from . import views

app_name = "challenges"
urlpatterns = [
    path("explore/", views.home, name="explore"),
    path("post/create/", views.create_challenge_post_view, name="create-post"),
]

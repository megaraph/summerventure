from django.urls import path

from .views import user_page

app_name = "users"

urlpatterns = [
    path("user/<int:id>", user_page, name="user_page"),
]

import pathlib
import uuid

from django.conf import settings

from django.db import models

User = settings.AUTH_USER_MODEL
AVATAR_STORAGE_FOLDER = "profile-pics"


def avatar_upload_handler(instance, filename):
    file_path = pathlib.Path(filename)
    new_file_name = str(uuid.uuid1())

    return f"{AVATAR_STORAGE_FOLDER}/{new_file_name}{file_path.suffix}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=avatar_upload_handler, null=False, blank=False)
    rating = models.PositiveIntegerField(null=False, blank=False, default=0)

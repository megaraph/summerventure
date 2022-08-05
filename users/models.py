import pathlib
import uuid

from django.conf import settings

from django.db import models

User = settings.AUTH_USER_MODEL
AVATAR_STORAGE_FOLDER = "profile-pics"
AVATAR_DEFAULT_SUFFIX = ".svg"


def avatar_upload_handler(instance, filename):
    file_path = pathlib.Path(filename)
    new_file_name = str(uuid.uuid1())

    return f"{AVATAR_STORAGE_FOLDER}/{new_file_name}{file_path.suffix}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=avatar_upload_handler, null=False, blank=False)
    rating = models.PositiveIntegerField(null=False, blank=False, default=0)

    def get_avatar_img(self):
        return f"{self.avatar.url}{AVATAR_DEFAULT_SUFFIX}"

    def get_rank(self):
        if self.rating > 2200:
            return "savior"

        ranks = {
            "recruit": range(0, 100),
            "attendant": range(100, 220),
            "carrier": range(220, 360),
            "messenger": range(360, 520),
            "specialist": range(520, 700),
            "mentor": range(700, 900),
            "adventurer": range(900, 1120),
            "master adventurer": range(1120, 1360),
            "explorer": range(1360, 1620),
            "royal explorer": range(1620, 1900),
            "challenger": range(1900, 2200),
        }

        for rank in ranks.keys():
            if self.rating in ranks[rank]:
                return rank

    def get_nav_rank_class(self):
        return f"nav-rank-{self.get_rank().replace(' ', '')}"

    def get_rank_class(self):
        return f"rank-{self.get_rank().replace(' ', '')}"

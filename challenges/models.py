import uuid
import pathlib
import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL
POST_STORAGE_FOLDER = "posts"


class ChallengeDifficulty(models.IntegerChoices):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class ChallengeApprovalStatus(models.TextChoices):
    APPROVED = ("a", "Approved")
    DECLINED = ("d", "Declined")
    PENDING = ("p", "Pending")


class Challenge(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    days = models.PositiveIntegerField(default=0)
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=30)
    duration = models.DurationField(null=False, blank=False)
    difficulty = models.IntegerField(choices=ChallengeDifficulty.choices)
    status = models.CharField(max_length=1, choices=ChallengeApprovalStatus.choices)

    def save(self, *args, **kwargs):
        days = self.days
        hours = self.hours
        minutes = self.minutes

        self.duration = datetime.timedelta(days=days, hours=hours, minutes=minutes)

        super().save(*args, **kwargs)


class AttemptStatus(models.TextChoices):
    DOING = ("p", "Doing")
    DONE = ("d", "Done")
    FAILED = ("f", "Failed")


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    expected_end_timestamp = models.DateTimeField(null=True, blank=True)
    actual_end_timestamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=AttemptStatus.choices)

    def save(self, *args, **kwargs):
        print("on save")
        super().save(*args, **kwargs)


def attempt_post_save(sender, created, instance, *args, **kwargs):
    if created:
        duration = instance.challenge.duration
        instance.expected_end_timestamp = instance.start_timestamp + duration
        instance.save()


post_save.connect(attempt_post_save, sender=Attempt)


def avatar_upload_handler(instance, filename):
    file_path = pathlib.Path(filename)
    new_file_name = str(uuid.uuid1())

    return f"{POST_STORAGE_FOLDER}/{new_file_name}{file_path.suffix}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    caption = models.CharField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to=False, null=False)


class PostUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    message = models.CharField(max_length=200, null=False, blank=False)


class CommentUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)


class CommentDownvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)

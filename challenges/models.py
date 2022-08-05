import uuid
import pathlib
import datetime
import requests

from urllib.parse import quote

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL
POST_STORAGE_FOLDER = "posts"

DIFFICULTIES = ["easy", "medium", "hard"]


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

    def get_absolute_url(self):
        return reverse("challenges:detail", kwargs={"id": self.pk})

    def get_all_attempts(self):
        return self.attempt_set.all()

    def get_all_posts(self):
        return self.post_set.all()

    def completion_rate(self):
        # done / (done + failed)
        completed_attempts = self.attempt_set.filter(status=AttemptStatus.DONE)
        failed_attempts = self.attempt_set.filter(status=AttemptStatus.FAILED)

        completed_count = completed_attempts.count()
        total = completed_count + failed_attempts.count()

        if total == 0:
            return total

        return round(completed_count / total, 2)

    def get_challenge_image(self, orientation="landscape"):
        quoted_title = quote(self.title)
        url = f"https://api.pexels.com/v1/search?query={quoted_title}&orientation={orientation}"
        res = requests.get(url=url)

        if res.json() is None or not res.ok:
            return "https://images.pexels.com/photos/1761282/pexels-photo-1761282.jpeg"

        try:
            size = "medium" if orientation == "portrait" else "large"
            img_obj = res.json().get("photos")[0]
            img = img_obj.get("src").get(size)
        except:
            return "https://images.pexels.com/photos/1761282/pexels-photo-1761282.jpeg"

        return img

    def get_featured_image(self):
        print(self.get_challenge_image(orientation="portrait"))
        return self.get_challenge_image(orientation="portrait")

    def difficulty_translate(self):
        return DIFFICULTIES[self.difficulty - 1]

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

    def get_absolute_url(self):
        return reverse(
            "challenges:post_detail",
            kwargs={"chal_id": self.challenge.id, "id": self.pk},
        )

    def get_all_comments(self):
        return self.comment_set.all()

    def get_upvote_count(self):
        return self.postupvote_set.count()

    def get_comment_count(self):
        return self.comment_set.count()

    def get_upvote_url(self):
        return reverse("challenges:post_upvote", kwargs={"id": self.pk})

    def has_upvoted_post(self, user):
        upvote = PostUpvote.objects.filter(post=self, user=user).first()
        return upvote is not None

    def remove_upvote(self, user):
        upvote = PostUpvote.objects.filter(post=self, user=user).first()
        upvote.delete()
        return True

    def upvote_post(self, user):
        if self.has_upvoted_post(user):
            success = self.remove_upvote(user)
            return success

        PostUpvote.objects.create(user=user, post=self)


class PostUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    pub_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    message = models.CharField(max_length=200, null=False, blank=False)

    def get_upvote_count(self):
        return self.commentupvote_set.count()

    def get_downvote_count(self):
        return self.commentdownvote_set.count()

    def get_vote_count(self):
        return self.get_upvote_count() - self.get_downvote_count()

    def get_reply_count(self):
        return self.comment_set.count()

    def get_upvote_url(self):
        return reverse(
            "challenges:comment_vote", kwargs={"id": self.pk, "action": "upvote"}
        )

    def get_downvote_url(self):
        return reverse(
            "challenges:comment_vote", kwargs={"id": self.pk, "action": "downvote"}
        )

    def has_upvoted_comment(self, user):
        upvote = CommentUpvote.objects.filter(comment=self, user=user).first()
        return upvote is not None

    def has_downvoted_comment(self, user):
        downvote = CommentDownvote.objects.filter(comment=self, user=user).first()
        return downvote is not None

    def remove_upvote(self, user):
        upvote = CommentUpvote.objects.filter(comment=self, user=user).first()
        upvote.delete()
        return True

    def remove_downvote(self, user):
        downvote = CommentDownvote.objects.filter(comment=self, user=user).first()
        downvote.delete()
        return True

    def vote_comment(self, user, action):
        if action == "upvote":
            if self.has_upvoted_comment(user):
                success = self.remove_upvote(user)
                return success

            if self.has_downvoted_comment(user):
                success = self.remove_downvote(user)
            CommentUpvote.objects.create(user=user, comment=self, post=self.post)
        else:
            if self.has_downvoted_comment(user):
                success = self.remove_downvote(user)
                return success
            if self.has_upvoted_comment(user):
                success = self.remove_upvote(user)
            CommentDownvote.objects.create(user=user, comment=self, post=self.post)


class CommentUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)


class CommentDownvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)

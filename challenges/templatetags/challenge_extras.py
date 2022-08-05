from django import template

from django.conf import settings
from challenges.models import Post, Comment

register = template.Library()

User = settings.AUTH_USER_MODEL


@register.simple_tag
def has_upvoted_post(user: User, post: Post):
    return post.has_upvoted_post(user)


@register.simple_tag
def has_upvoted_comment(user: User, comment: Comment):
    return comment.has_upvoted_comment(user)


@register.simple_tag
def has_downvoted_comment(user: User, comment: Comment):
    return comment.has_downvoted_comment(user)

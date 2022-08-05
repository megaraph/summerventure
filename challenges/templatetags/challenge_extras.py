from django import template

from django.conf import settings
from challenges.models import Post

register = template.Library()

User = settings.AUTH_USER_MODEL


@register.simple_tag
def has_upvoted(user: User, post: Post):
    return post.has_upvoted_post(user)

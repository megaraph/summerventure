import random

from django.utils import timezone


def get_featured_challenges(query_set, quantity):
    today = timezone.now()
    seed = today.year + today.month + today.day + today.hour

    random.seed(seed)
    return random.sample(list(query_set), quantity)

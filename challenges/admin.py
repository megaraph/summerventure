from django.contrib import admin

from .models import (
    Challenge,
    Attempt,
    Post,
    PostUpvote,
    Comment,
    CommentUpvote,
    CommentDownvote,
)


class ChallengeAdmin(admin.ModelAdmin):
    readonly_fields = ("duration",)


admin.site.register(Challenge, ChallengeAdmin)


class AttemptAdmin(admin.ModelAdmin):
    readonly_fields = (
        "expected_end_timestamp",
        "actual_end_timestamp",
    )


admin.site.register(Attempt, AttemptAdmin)

admin.site.register(Post)
admin.site.register(PostUpvote)
admin.site.register(Comment)
admin.site.register(CommentUpvote)
admin.site.register(CommentDownvote)

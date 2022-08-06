from django import forms

from .models import Post

# class PostCreationForm(forms.Form):
#     caption = forms.CharField(
#         label="Caption",
#         max_length=200,
#         widget=forms.Textarea(attrs={"placeholder": "Write a caption"}),
#     )

#     image = forms.ImageField(label="Image")
#     image.widget.attrs.update({"class": "image-input"})

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         return cleaned_data


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["caption"].widget = forms.Textarea(
            attrs={"placeholder": "Write a caption"}
        )
        self.fields["image"].widget.attrs.update({"class": "image-input"})


class CommentCreationForm(forms.Form):
    # comment-textarea
    message = forms.CharField(
        max_length=200,
        widget=forms.Textarea(
            attrs={"placeholder": "Write a comment", "class": "comment-textarea"}
        ),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

from django import forms


from .models import Post


class PostForm(forms.ModelForm):
    published = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "published",
        ]

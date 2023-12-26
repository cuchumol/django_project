from django import forms
from .models import Post, Comment
#from django.urls import reverse

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'is_published')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

    widgets = {
        'author': forms.HiddenInput(),  
        'text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    }
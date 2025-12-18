from django import forms
from .models import Post, Comment, Newsletter

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ('title', 'content',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }

        labels = {
            'title': 'Tytuł',
            'content': 'Treść'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

        labels = {
            'text': 'Komentarz'
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Twój email'})
        }
        labels = {
            'email': ''
        }
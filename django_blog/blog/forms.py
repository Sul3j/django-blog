from django import forms
from .models import Post, Comment

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
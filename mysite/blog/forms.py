from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        labels = {
            'name': '',
            'email': '',
            'body': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'label': '','class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша электронная почта'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
        }


class EmailPostForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=25, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Ваше имя'
            }
        )
    )
    to = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта пункта назначения'
            }
        )
    )
    comments = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Тут Ваш комментарий'
            }
        )
    )
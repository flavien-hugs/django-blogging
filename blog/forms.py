from django import forms
from django.forms import TextInput, EmailInput, Textarea
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
        'placeholder':'Name*'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email*'}))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'cols':"30", 'rows':"10", 'placeholder':'Message'
        }))
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
        'placeholder':'Search', 'type':'search'}))

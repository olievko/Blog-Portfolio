from django.forms import ModelForm, Textarea, TextInput
from django import forms
from .models import Comment


class ContactForm(forms.Form):
    contact_name = forms.CharField(max_length=100, widget=forms.TextInput())
    contact_email = forms.EmailField(widget=forms.TextInput())
    subject = forms.CharField(max_length=100, widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())
    cc_myself = forms.BooleanField(required=False)


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))
    to = forms.EmailField(widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '100', 'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': TextInput(attrs={'size': 100}),
            'email': TextInput(attrs={'size': 100}),
            'body': Textarea(attrs={'cols': 100}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()

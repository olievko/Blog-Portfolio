from django.forms import ModelForm, Textarea, TextInput
from django import forms
from .models import Comment


class ContactForm(forms.Form):
    contact_name = forms.CharField(
        max_length=250,
        label='Contact Name',
        widget=forms.TextInput(attrs={
            "class": "w3-input w3-border",
        })
    )
    contact_email = forms.EmailField(
        label='Contact Email',
        widget=forms.TextInput(attrs={
            "class": "w3-input w3-border",
        })
    )
    subject = forms.CharField(
        max_length=250,
        label='Subject',
        widget=forms.TextInput(attrs={
            "class": "w3-input w3-border",
        })
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            "class": "w3-input w3-border",
        })
    )
    cc_myself = forms.BooleanField(required=False)


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w3-input w3-border '
        })
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'w3-input w3-border'
        })
    )
    to = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'w3-input w3-border'
        })
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w3-input w3-border'
        })
    )


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'w3-input w3-border'
        })
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts..',
        })
    )

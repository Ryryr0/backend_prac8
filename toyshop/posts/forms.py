from django import forms

from .models import Post, PostFiles


class PostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    is_published = forms.TypedChoiceField(label='Privacy', choices=Post.STATUS, coerce=int,
                                          empty_value=Post.STATUS.PUBLISHED, initial=Post.STATUS.PUBLISHED)
    content = forms.CharField(label='Description', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-input text-input'}))
    file = forms.FileField(label='Upload a File', required=False, widget=forms.FileInput(attrs={'id': 'fileInput'}))

    class Meta:
        model = Post
        fields = ['title', 'is_published', 'content', 'file']

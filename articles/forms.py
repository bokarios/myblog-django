from django import forms
from .models import Post

class CreateForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    slug = forms.CharField(max_length=30)
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content','image')

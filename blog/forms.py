from django import forms
from .models import Post
from django.contrib.auth import get_user
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('auther',)
        fields = '__all__' 
        
    def clean_slug(self):
        return self.cleaned_data['slug'].lower()
    def save(self,request, commit=True):
        post=super().save(commit=False)
        if not post.pk:
            post.auther = get_user(request)
        if commit:
            post.save()
            self._save_m2m()
        return post
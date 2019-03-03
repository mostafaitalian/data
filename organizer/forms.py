from django import forms
from .models import Tag, Startup, NewsLink
from django.core.exceptions import ValidationError
from organizer.mixin import CleanSlugNameMixin
class TagForm1(CleanSlugNameMixin, forms.Form):
    
    name = forms.CharField(max_length=31)
    slug = forms.SlugField(max_length=31, help_text='label for url config')
    
    
    def save(self):
        new_tag = Tag.objects.create(name = self.name, slug=self .slug)
        return new_tag
    
    
    def clean_name(self):
        new_name = self.cleaned_data['name'].lower()
        return new_name
    
    
class TagForm(CleanSlugNameMixin, forms.ModelForm):
    
    class Meta:
        model=Tag
        #fields = ['name', 'slug']
        fields = '__all__'
    
    def clean_name(self):
        new_name = self.cleaned_data['name'].lower()
        return new_name

class StartupForm(CleanSlugNameMixin, forms.ModelForm):
    
    class Meta:
        model=Startup
        fields = '__all__'


class NewsLinkForm(CleanSlugNameMixin, forms.ModelForm):
    
    class Meta:
        model = NewsLink
        fields = '__all__'
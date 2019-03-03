from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from user.utils import ActivationMailFormMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import  Profile
from django.forms import ModelForm
from django import forms
class UserCreationForm(ActivationMailFormMixin, BaseUserCreationForm):
    name = forms.CharField(max_length=255,help_text=("The name displayed on your public profile."))
    def clean_username(self):
        name = self.cleaned_data['name']
        disallowed=('login', 'logout', 'password', 'activate', 'profile', 'create', 'disable')
        if name in disallowed:
            raise ValidationError('user name you are already choosed not allowed, do not chooce from the following list {}'.format(*disallowed))
        return name
    
    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('name', 'email')
        
    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:
            user.is_active=False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        #Profile.objects.update_or_create(user=user, slug=slugify(self.clean_username()))
        Profile.objects.update_or_create(user=user, defaults={'name':self.cleaned_data['name'],
                                                              'slug':slugify(user.get_username())})
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user
class ProfileForm(ModelForm):
    
    class Meta:
        model=Profile
        fields = ('slug', 'about')
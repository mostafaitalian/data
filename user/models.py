from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.shortcuts import reverse
from _datetime import date
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, unique=True)
    about = models.TextField()
    name = models.CharField(max_length=255)
    joined = models.DateTimeField('Date joined', auto_now_add=True)
    def get_absolute_url(self):
        return reverse_lazy('userr:user_profile_public_detail', kwargs={'slug':self.slug})
    def get_update_url(self):
        return reverse_lazy('userr:user_profile_update')
    def __str__(self):
        return self.user.get_username()
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          is_active=True,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extrafields):
        return self._create_user(email, password, **extrafields)
    def create_superuser(self, email, password, **extrafields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extrafields)
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField('user email', max_length=255, unique=True)
    
    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='disignate whether the user can use the admin site or not')
    is_active = models.BooleanField('enable user or disable',
                                    default=True,
                                    help_text='if you want to delete user make it false')
    USERNAME_FIELD = 'email'
    objects = UserManager()
    class Meta(AbstractBaseUser.Meta):
        swappable = 'AUTH_USER_MODEL'
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return self.profile.get_abolute_url()
    
    def get_full_name(self):
        return self.profile.name
    
    def get_short_name(self):
        return self.profile.name
    
    def published_posts(self):
        return self.blog_posts.filter(pub_date__lt=date.today())
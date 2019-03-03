from django.db import models
from organizer.models import  Startup, Tag
from django.shortcuts import reverse
from django.urls.base import reverse_lazy
from django.conf import settings
from datetime import datetime
from django.db.models.signals import m2m_changed
# Create your models here.
class BasePostManager(models.Manager):
    def get_by_natural_key(self, pub_date, slug):
        return self.get(pub_date=pub_date, slug=slug)
    def published(self):
        return self.filter(pub_date__lt=datetime.today())
class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    def published(self):
        return self.get_queryset().filter(pub_date__lt=datetime.today())
class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(pub_date__lt= datetime.now())
PostManagerr = BasePostManager.from_queryset(PostQuerySet)
    
class Post(models.Model):
    auther = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63,help_text='A label for url config', unique_for_month='pub_date')
    text = models.TextField()
    pub_date = models.DateField('date published')
    startups = models.ManyToManyField(to=Startup, related_name='blog_posts')
    tags = models.ManyToManyField(to=Tag, related_name='blog_posts')
    def formatted_title(self):
        return self.title.title()
    def short_text(self):
        if len(self.text)>20:
            short = ' '.join(self.text.split()[:20])
            short += '....'
        else:
            short = self.text
        return short 
    
    def natural_key(self):
        return self.pub_date,self.slug
    natural_key.dependencies = ['organizer.startup','organizer.tag','user.user']
    #objects = PostQuerySet.as_manager()
    objects = PostManager()
    def __str__(self):
        return '{}-on-{}'.format(self.title, self.pub_date.strftime('%y-%m-%d'))
    def get_absolute_url(self):
        return reverse('blog:blog_post_detail', kwargs={'year': self.pub_date.year,
                                                        'month': self.pub_date.month,
                                                        'slug':self.slug})
    def get_update_url(self):
        return reverse('blog:blog_post_update', kwargs={'slug': self.slug})
    def get_archive_year_url(self):
        return reverse('blog:blog_post_archive_year', kwargs={'year': self.pub_date.year})
    def get_archive_month_url(self):
        return reverse_lazy('blog:blog_post_archive_url', kwargs={'year': self.pub_date.year, 'month': self.pub_date.month})
    def get_delete_url(self):
        return reverse_lazy('blog:blog_post_delete', kwargs={'year':self.pub_date.year, 'month':self.pub_date.month, 'slug':self.slug})

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
        permissions = (('view_future_post','can view unpublished posts'),)
'''class Th(models.Model):
    startups = models.ForeignKey(Startup, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        auto_created=True'''
    


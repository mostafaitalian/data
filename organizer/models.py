from django.db import models
from django.template.defaultfilters import title
from django.shortcuts import reverse
from django.urls import reverse_lazy
from datetime import datetime
from django.utils.functional import cached_property
from urllib import parse
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for url config') 
    
    def __str__(self):
        return self.name
    class Meta:
        ordering=['name']
        
    def get_absolute_url(self):
        return reverse("organizer:organizer_tag_detail", kwargs={'slug':self.slug})
    def get_update_url(self):
        return reverse('organizer:organizer_tag_update', kwargs={'slug':self.slug})
    def get_delete_url(self):
        return reverse('blog:blog_post_delete', kwargs={'slug': self.slug})
        
class Startup(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='a label for url config')
    description = models.TextField()
    founded_date = models.DateField('data founded')
    contact = models.EmailField()
    website = models.URLField()
    tags = models.ManyToManyField(to=Tag)
    @cached_property
    def published_posts(self):
        return self.blog_posts.filter(pub_date__lt=datetime.today())
    def __str__(self):
        return self.name
    def get_update_url(self):
        return reverse('organizer:organizer_startup_update', kwargs={'slug':self.slug})
    def get_absolute_url(self):
        return reverse('organizer:organizer_startup_detail', kwargs={'slug':self.slug}) 
    def get_feed_atom_url(self):
        return reverse('organizer:organizer_startup_feed_atom', kwargs={'startup_slug':self.slug})
    def get_feed_rss_url(self):
        return reverse('organizer:organizer_startup_feed_rss', kwargs={'startup_slug':self.slug})
    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'
class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(default=title)
    pub_date = models.DateField('data published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(to=Startup, on_delete=models.CASCADE)

    def __str__(self):
        return '{}--{}'.format(self.startup, self.title)
    def get_absolute_url(self):
        return reverse_lazy("organizer:organizer_newslink_detail", kwargs={'slug':self.slug})
    def get_update_url(self):
        return reverse('organizer:organizer_startup_update', kwargs={'slug': self.slug})
    def description(self):
        return 'created on {0:%A,%B}-{0.day}-{0.%Y} and hosted {1}{2}'.format(self.pub_date, parse.urlparse(self.link).netloc, parse.urlparse(self.link)[1])
    class Meta:
        
        verbose_name = 'new_article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'startup')
from django.contrib.messages import success
from django.db.models.signals import m2m_changed
from blog.models import Post
from organizer.models import Tag, NewsLink,Startup
from django.dispatch import receiver
from django.apps import apps as suorganizer_apps
blog_app = suorganizer_apps.get_app_config('blog')
Post = blog_app.get_model('Post')
@receiver(m2m_changed)
def add_extra_tags(sender, **kwargs):
    action = kwargs.get('action')
    if action=='post_add' or action=='pre add':
        reverse=kwargs.get('reverse')
        if not reverse:
            post = kwargs.get('instance')
            startup_pk_set = kwargs.get('pk_set')
            tag_pk_set = Tag.objects.filter(
                startup__in=startup_pk_set).values_list(
                    'pk', flat=True).distinct().iterator()
            #post.tags.add(*tag_pk_set)
            post.tags.add()
        else:
            startup = kwargs.get('instance')
            tag_pk_set = tuple(startup.tags.values_list('pk', flat=True)).iterator()
            PostModel = kwargs.get('model')
            post_pk_set = kwargs.get('pk_set')
            post_dict = PostModel.objects.in_bulk(post_pk_set)
            for post in post_dict:
                post.tags.add(*tag_pk_set)
            


sender=Post.startups.through
print(sender)        
m2m_changed.connect(add_extra_tags, sender)


post1 = Post.objects.get(pk=1)
post1.tags
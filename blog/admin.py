from django.contrib import admin
from .models import Post
from django.db.models import Count, Max
# Register your models here.
#admin.site.register(Post)
from datetime import datetime
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def tags_count(self,post):
        return post.tags.count()
    tags_count.short_description='number of tags'
    tags_count.admin_order_field = 'tags_number'
    list_display = ('title', 'pub_date', 'tags_count') #set the fields to be shown in thelist of posts
    date_hierarchy = 'pub_date' #set the date field to be used to make a calender-like
    list_filter = ('title','pub_date')
    search_fields = ('title', 'text')
    fieldsets=((None,{'fields':('title','text','slug','auther', 'pub_date')}),('Related',{'fields':('tags','startups')}))
    prepopulated_fields = {'slug':('title',)}
    filter_horizontal = ('tags',)
    filter_vertical = ('startups',)
    
    def get_queryset(self, request):
        queryset=super().get_queryset(request)
        if not request.user.has_perm('view_future_posts'):
            queryset = queryset.filter(pub_date__lt=datetime.now())
        return queryset.annotate(tags_number=Count('tags'))
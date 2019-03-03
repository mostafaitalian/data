from django.contrib import admin
from .models import Tag, Startup, NewsLink
# Register your models here.

admin.site.register(Tag)
admin.site.register(Startup)
admin.site.register(NewsLink)
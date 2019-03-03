"""suorganizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from suorganizer.views import redirect_view
from django.urls import reverse, path, include
from django.contrib.flatpages import urls as flatpage_urls
import debug_toolbar
from blog.feed import AtomPostFeed, Rss2PostFeed
#import organizer.urls
#import user.urls
admin.site.site_header='admin startup organizer'
admin.site.site_title = 'startup organizer'
sitenews = [path('atom', AtomPostFeed(), name='atom'),
            path('rss', Rss2PostFeed(), name='rss')]
urlpatterns = [
    path('user/', include('user.urls', namespace='userr')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('page', include(flatpage_urls)),
    path('admin/', admin.site.urls),
    path('', redirect_view),
    path('',include('organizer.urls', namespace='organizer')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('newslink/', include('organizer.startup', namespace='organizzer')),
    path('feeds/', include(sitenews))
]

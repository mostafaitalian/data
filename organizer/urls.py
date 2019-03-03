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
from django.urls import path, include
from django.conf.urls import url
from organizer.views import home, tag_detail, tag_list, startup_list, startup_detail, create_tag
from organizer import views
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .feeds import AtomStartupFeed, RssStartupFeed
app_name = 'organizer'

urlpatterns = [path('tag/', views.TagList.as_view(), name = 'organizer_tag_list'),
               url(r'^tags/create/$', views.TagCreate.as_view(), name='organizer_tag_create'),
               url(r'^startup/create/$', views.StartupCreate.as_view(), name='organizer_startup_create'),
               url(r'^newslink/create/$', views.NewsLinkCreate.as_view(), name='organizer_newslink_create'),
               path('tag/<str:slug>', views.TagDetail.as_view(), name='organizer_tag_detail'),
               url(r'^tag/$', home, name='tag_list'),
               path('startup/', views.StartupList.as_view(), name = 'organizer_startup_list'),
               path('startup/<str:slug>/', views.StartupDetail.as_view(), name = 'organizer_startup_detail'),
               path('tag/<str:slug>/update', views.TagUpdate.as_view(), name='organizer_tag_update'),
               path('startup/<str:slug>/update', views.StartupUpdate.as_view(), name='organizer_startup_update'),
               path('NewsLink/<str:slug>/update', views.NewsLinkUpdate.as_view(), name='organizer_startup_update'),
               path('tag/<str:slug>/delete', views.TagDelete.as_view(), name='organizer_tag_delete'),
               path('redirect/', RedirectView.as_view(pattern_name='blog:blog_post-list')),]
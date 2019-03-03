from django.urls import path
from organizer import views
from organizer.views import NewsLinkDelete
from .feeds import AtomStartupFeed, RssStartupFeed
app_name = 'organizer'

urlpatterns = [
    path('<str:startup_slug>/add_article_link',views.NewsLinkCreate.as_view(), name='organizer_newslink_create'),
    path('<str:startup_slug>/<str:newslink_slug>/delete', views.NewsLinkDelete.as_view(), name='organizer_newslink_delete'),
    path('<str:startup_slug>/<str:newslink_slug>/update', views.NewsLinkUpdate.as_view(),name='organizer_newslink_update'),
    path('<str:startup_slug>/atom', AtomStartupFeed(), name='organizer_startup_feed_atom'),
    path('<str:startup_slug>/rss', RssStartupFeed(), name='organizer_startup_feed_rss')
    ]
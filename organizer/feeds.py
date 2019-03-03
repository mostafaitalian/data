from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from .models import NewsLink, Tag, Startup
from .utils import BaseStartupFeedMixin

class AtomStartupFeed(BaseStartupFeedMixin, Feed):
    feed_type = Atom1Feed

class RssStartupFeed(BaseStartupFeedMixin, Feed):
    feed_type = Rss201rev2Feed

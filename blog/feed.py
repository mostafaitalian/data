from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .utils import BasePostFeedMixin

class AtomPostFeed(BasePostFeedMixin,Feed):
    feed_type = Atom1Feed
class Rss2PostFeed(BasePostFeedMixin, Feed):
    feed_type = Rss201rev2Feed
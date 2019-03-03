from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Post
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponseRedirect
from django.views.generic.dates import DateMixin
from .utilss import YearMixin, MonthMixin, _date_from_string, AllowFuturePermissionMixin
class PostGetMixin:
    year_url_kwarg = 'year'
    month_url_kwarg = 'month'
    day_url_kwarg = 'day'
    date_field = 'pub_date'
    errors ={'error_kwargs': ' you should put the year and month and slug in the {} url'}    
    
    def get_object(self, queryset=None):
        date_field = self.date_field
        slug_field = self.get_slug_field()
        year = self.kwargs.get(self.year_url_kwarg)
        month = self.kwargs.get(self.month_url_kwarg)
        day = self.kwargs.get(self.day_url_kwarg)
        slug = self.kwargs.get('slug')
        dict_filter = {date_field+'__year' : year,
                       date_field+'__month' : month,
                       slug_field : slug}
        if year is None or month is None or slug is None:
            raise AttributeError(self.errors.get('error_kwargs').format(self.__class__.__name__))
        
        return get_object_or_404(Post, **dict_filter)
    
class PostMixin2Mixin:
    model = Post
    date_field = 'pub_date'
    errors ={'error_kwargs': ' you should put the year and month and slug in the {} url'}    
    
    def get_object(self, queryset=None):
        date_field = self.date_field
        slug_field = self.get_slug_field()
        year = self.kwargs.get(self.year_url_kwarg)
        month = self.kwargs.get(self.month_url_kwarg)
        day = self.kwargs.get(self.day_url_kwarg)
        slug = self.kwargs.get('slug')
        dict_filter = {date_field+'__year' : year,
                       date_field+'__month' : month,
                       slug_field : slug}
        if year is None or month is None or slug is None:
            raise AttributeError(self.errors.get('error_kwargs').format(self.__class__.__name__))
        
        if queryset is None:
            queryset = self.get_queryset()
            queryset = queryset.filter(**dict_filter)
            try:
                obj = queryset.get()
            except ObjectDoesNotExist:
                raise Http404(self.errors['error_kwargs'].format(queryset.model._meta_verbose_name))
class PostGet3Mixin(YearMixin, MonthMixin, DateMixin, AllowFuturePermissionMixin):
    date_field = 'pub_date'
    model = Post
    
    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field(date)
        if self.uses_datetime_field():
            since = self._make_date_lookup_arg(date)
            until = self._make_date_lookup_arg(self.get_next_month(date))
            return {'%s__gte' % date_field : date,
                    '%s__lt' % date_field : self.get_next_month(date) }
        else:
            return {'%s__gte' % date_field : date,
                    '%s__lt' % date_field : self.get_next_month(date) }
    def get_object(self,queryset=None):
        year = self.get_year()
        month = self.get_month()('month')
        slug = self.kwargs.get('slug')
        date = _date_from_string(year, self.get_year_format(), month, self.get_month_format)
        
        if queryset is None:
            queryset = self.get_queryset()
            if (not self.get_allow_future() and date > date.today()):
                raise Http404("{}dates can not be greater than today {}.allow_future is false".format(self.__class__.__name__,queryset.model._meta_verbose_name_plural))
        
        dict_filter = self._make_single_date_lookup(date)
        queryset = queryset.filter(**dict_filter)
        return super().get_object(queryset)

class PostFormValidMixin:
    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())
    
class BasePostFeedMixin:
    title = 'latest startup organizer blog posts'
    link = reverse_lazy('blog:blog_post_list')
    description = subtitle = 'stayup tuned for the latest startup posts'
    
    def items(self):
        return Post.objects.published()[:10]
    def item_title(self,item):
        return item.formatted_title()
    def item_description(self, item):
        return item.short_text()
    def item_link(self, item):
        return item.get_absolute_url()

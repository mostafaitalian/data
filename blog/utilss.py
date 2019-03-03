from django.views.generic.dates import YearMixin as BaseYearMixin
from django.views.generic.dates import _date_from_string, MonthMixin as BaseMonthMixin

from django.http import Http404

class YearMixin(BaseYearMixin):
    year_query_kwarg = 'year'
    year_url_kwarg = 'year'
    
    def get_year(self):
        year = self.year
        if year is None:
            year = self.kwargs.get(self.year_url_kwarg,
                                   self.request.Get.get(self.year_query_kwarg))
        if year is None:
            raise Http404('can not get year from url path and/or query url')
        return year
    
class MonthMixin(BaseMonthMixin):
    month_url_kwarg = 'month'
    month_query_url = 'month'
    month_format = '%m'
    def get_month(self):
        month = self.month
        if month is None:
            month = self .kwargs.get(self.month_url_kwarg,
                                     self.request.Get.get(self.month_query_url))
        if month is None:
            raise Http404('can not find month in path or query')
        return month
class AllowFuturePermissionMixin:
    def get_allow_future(self):
        return self.request.user.has_perm('blog.view_future_post')
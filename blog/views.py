from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from organizer import mixin
from django.views.generic import YearArchiveView, MonthArchiveView, ArchiveIndexView, DateDetailView
from django.views.generic import DeleteView, DetailView, UpdateView
from blog.models import Post
from blog.forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from botocore.vendored.requests.api import post
from .utils import PostGetMixin, PostGet3Mixin
from user.decorators import require_authenticated_permission, class_login_decorator
from .utilss import AllowFuturePermissionMixin
# Create your views here.
def post_list(request):
    post_list = Post.objects.all()
    
    return render(request, 'blog/post-list.html', {'post_list': post_list})

@require_http_methods(['GET', 'HEAD'])
def post_detail(request, slug):
    post = get_object_or_404(Post, slug__iexact=slug)
    
    return render(request, 'blog/post_detail.html', {'post' : post})

class PostList(View):
    template_name = 'blog/post-list.html'
    def get(self, request):
        
        post_list = Post.objects.all()
        return render(request, self.template_name, {'post_list': post_list})
    
    @staticmethod
    def as_view(cls, **initkwargs):
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            return self.dispatch(request, *args, **kwargs)
        return view
@class_login_decorator
class PostCreate(CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    model= Post
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(request)
            return redirect(new_post)
        else:
            return render(request, self.template_name,{'form':form})

#class PostUpdate(mixin.ObjectUpdateMixin, View):
class PostUpdate(AllowFuturePermissionMixin, PostGetMixin, UpdateView):
    date_field = 'pub_date'
    form_class = PostForm
    template_name = 'blog/post_form_update.html'
    model = Post
class PostArchiveView(AllowFuturePermissionMixin, YearArchiveView):
    model = Post
    date_field = 'pub_date'
    make_object_list = True
class PostDelete(AllowFuturePermissionMixin, PostGetMixin, DeleteView):
    date_field = 'pub_date'
    form_class= PostForm
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    def get_success_url(self):
        return reverse('blog:blog_post-list')
class PostArchiveMonth(AllowFuturePermissionMixin, MonthArchiveView):
    model = Post
    date_field = 'pub_date'
    month_format = '%m'
class PostaList(AllowFuturePermissionMixin, ArchiveIndexView):
    model = Post
    allow_empty = True
    date_field = 'pub_date'
    make_object_list = True
    context_object_name = 'post_list'
    date_list_period = 'year'
    paginated_by =2
    template_name = 'blog/post-list.html' 
    
class PostoList(ListView):
    model = Post
    paginated_by = 3
    
class PostaDetail(AllowFuturePermissionMixin, DateDetailView):
    date_field = 'pub_date'
    model = Post
    month_format = '%m'
    
    def get_day(self):
        return '1'
    
    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field()
        return {date_field + '__year' : date.year,
                date_field + '__month' : date.month}
        
class PostDetail(PostGetMixin, DetailView):
    
    model = post
      
    

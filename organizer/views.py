from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from .models import Tag, Startup, NewsLink
from django.template import Template, loader
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from .forms import TagForm, StartupForm, NewsLinkForm
from django.http import HttpResponseRedirect
from django.views import View
from .mixin import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from organizer.forms import StartupForm, NewsLinkForm, TagForm
from django.core.paginator import Paginator
from django.core.paginator import  EmptyPage,PageNotAnInteger
from .utils import DetailView
from . import mixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import PermissionDenied
# Create your views here.
from django.views.generic import CreateView,UpdateView,DeleteView,View
from django.views.generic import ListView
from django.views.defaults import permission_denied
from user.decorators import custom_login_decorator, require_authenticated_permission
from amqp.spec import method
class TagDetail(DetailView):
    model = Tag

class StartupDetail(DetailView):
    model = Startup
    template_name = 'organizer/startup_detail.html'
    context_object_name = 'startup'
    
def home(request):
    tag_list = Tag.objects.all()
    template = loader.get_template('organizer/tag_list.html')
    output = template.render({'tag_list': tag_list})
    return HttpResponse(output)

def tag_list(request):
    tag_list = Tag.objects.all()
    return render(request, 'organizer/tag_list.html', {'tag_list': tag_list})

def tag_detail(request, slug):
    try:
        tag = Tag.objects.get(slug__iexact=slug)
    except Tag.DoesNotExist:
        raise Http404
        #return HttpResponseNotFound('<h1>no such tag with this name</h1>')
    template = loader.get_template('organizer/tag-detail.html')
    output = template.render({'tag': tag})
    return HttpResponse(output)
def startup_list(request):
    startup_list = Startup.objects.all()
    return render(request, 'organizer/startup_list.html', {'startup_list' : startup_list})
def startup_detail(request, slug):
    startup = get_object_or_404(Startup, slug__iexact=slug)
    template = loader.get_template('organizer/startup-detail.html')
    return HttpResponse(template.render({'startup': startup}))
def create_tag(request):
    
    if request.method == 'POST':
        form = TagForm(request.POST)
        
        if form.is_valid():
            new_tag = form.save()
            
            #return HttpResponseRedirect(new_tag.get_absolute_url())
            #return HttpResponseRedirect(reverse_lazy('organizer:organizer_tag_detail', kwargs={'slug':new_tag.slug}))
            return redirect(new_tag)      
        else:
            output = render(request,'organizer/tag_form.html', {'form' : form})
            form = TagForm()
            return output
            
                
    else:
        form = TagForm()
        return render(request,'tag_form.html', {'form' : form, 'errors':form.errors })
    
    
    
def in_contributors_group(user):
    if user.groups.filter(name='contributors').exists():
        return True
    else:
        raise permission_denied
class TagCreate(CreateView):
    form_class = TagForm
    template_name = 'organizer/tag_form2.html'
    @method_decorator(login_required)
    @method_decorator(permission_required('organizer.add_tag',raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)
@require_authenticated_permission('organizer.add_startup')
class StartupCreate(CreateView):
    form_class = StartupForm
    template_name = 'organizer/startup_form.html'
    @method_decorator(custom_login_decorator)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class NewsLinkCreate(CreateView):
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_form.html'

class TagUpdate(UpdateView):
    form_class = TagForm
    template_name = 'organizer/tag_form_update.html'
    model = Tag
    @method_decorator(custom_login_decorator)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
class StartupUpdate(UpdateView):
    form_class = StartupForm
    template_name = 'organizer/Startup_form_update.html'
    model = Startup
class NewsLinkUpdate(UpdateView):
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_form_update.html'
    model = NewsLink
class TagDelete(DeleteView):
    model = Tag
    form_class = TagForm
    template_name = 'organizer/tag_confirm_delete.html'
    success_url = reverse_lazy('organizer:organizer_tag_list')
    
class StartupList(View, mixin.PageLinkMixin):
    template_name = 'organizer/startup_list.html'
    paginated_by = 2
    page_kwarg = 'page'
    startups = Startup.objects.all()

    def get(self, request):
        
        paginator = Paginator(self.startups, self.paginated_by)
        page_number = request.GET.get(self.page_kwarg)
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            page = paginator.get_page(1)
        except PageNotAnInteger:
            page = paginator.get_page(paginator.num_pages())
        if page.has_other_pages():
            if page.has_next():
                next_url = '?{}={}'.format(self.page_kwarg, page.next_page_number())
            else:
                next_url = None
            if page.has_previous():
                previous_url = '?{}={}'.format(self.page_kwarg, page.previous_page_number())
            else:
                previous_url = None
            
            
            return render(request, self.template_name, {'startup_list':page, 'next':next_url, 'previous':previous_url}) 
        else:
            return render(request, self.template_name, {'startup_list':page}) 

class NewssLinkUpdate(mixin.UpdateView):
    form_class = NewsLinkForm
    model =NewsLink
       
class TagList(ListView):
    page_kwarg = 'page'
    paginated_by = 4
    template_name = "organizer/tag_list.html"
    queryset = Tag.objects.all()
    model = Tag
    def get(self, request,**kwargs):
        paginator = Paginator(self.queryset, self.paginated_by)
        try:
            num=request.GET.get('page')
            page = paginator.page(num)
        except PageNotAnInteger:
            page = paginator.page(1)
        return render(request, self.template_name, {'tag_list': page, 'paginator':paginator})
class NewsLinkDelete(DeleteView):
    form_class = NewsLinkForm
    model = NewsLink
    def get_success_url(self):
        return reverse('organizer:organizer_startup_detail', kwargs = {'slug': self.object.startup.slug})
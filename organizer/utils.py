from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from .models import Startup
class DetailView(View):
    template_name = ''
    model = None
    context_object_name = ''
    template_name_suffix = '_detail'

    def get(self, request, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        template = self.get_template_name()
        context = self.get_context_data()
        return render(request, template, context)
    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        elif isinstance(self.object, self.model):
            return self.object._meta.model_name
        else:
            return None
    def get_template_name(self):
        if self.template_name:
            return self.template_name
        return '{}/{}{}.html'.format(self.object._meta.app_label, self.object._meta.model_name, self.template_name_suffix)
    def get_context_data(self):
        context = {}
        if self.object:
            context_object_name = self.get_context_object_name()
            if context_object_name:
                context[context_object_name] = self.object
        return context
    def get_object(self):
        slug = self.kwargs.get('slug')
        if slug is None:
            raise AttributeError("{} except {} parameters from url configuration".format(self.__class__.__name__, 'slug'))
        if self.model:
            return get_object_or_404(self.model, slug__iexact=slug)
        else:
            raise ImproperlyConfigured("{} needs {} attribute to work".format(self.__class__.__name__, 'model'))
        
        
        '''def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template_name, {self.context_object_name: obj})'''
       
       
class CreateView(View):
    form_class = None
    template_name = ''
    
    def get(self,request):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return HttpResponseRedirect(new_obj.get_absolute_url())
        else:
            return render(request, self.template_name, {'form':bound_form})
        
class UpdateView(View):
    form_class = None
    model = None
    template_name = ''
    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        context = {'form' : self.form_class(instance=obj), 'obj' : obj}
        return render(request, self.template_name, context)
    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            new_obj = form.save()
            #return HttpResponseRedirect(new_obj.get_absolute_url())
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': form})
        
        
class DeleteView(View):
    form_class = None
    model = None
    success_url = ''
    template_name=''
    
    def get(self,request, slug):
        obj = get_object_or_404(self.model, slug__iexact = slug)
        form = self.form_class(instance=obj)
        return render(request, self.template_name, {'form' : form, 'obj' : obj})
    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact = slug)
        obj.delete()
        return HttpResponseRedirect(self.success_url)
class BaseStartupFeedMixin():
    def get_object(self,request, startup_slug):
        return get_object_or_404(Startup, slug__iexact=startup_slug)
    def items(self, startup):
        return startup.newslink_set.all()[:10]
    def item_title(self, newslink):
        return newslink.title
    def item_link(self, newslink):
        return newslink.link
    def item_description(self, newslink):
        return newslink.description
    def description(self, startup):
        return "News related to {}".format(startup.name)
    def link(self, startup):
        return startup.get_absolute_url()
    def subtitle(self, startup):
        return self.description(startup)
    def title(self, startup):
        return startup.name
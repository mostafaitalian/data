from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView as BaseUpdateView
from django.core.paginator import Paginator
from .models import Tag
class CleanSlugNameMixin:
    
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('slug can not be create')
        return new_slug

class ObjectCreateMixin:
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
        
class ObjectUpdateMixin:
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
        
        
class ObjectDeleteMixin:
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
class UpdateView(BaseUpdateView):
    template_name_suffix = 'form_update'
    
    
class PageLinkMixin:
    page_kwarg='page'
    context_object_name = ''
    model = None
    model_name = ''
    paginated_by =3
    queryset=None
    def _page_urls(self, page_number):
        return '?{}={}'.format(self.page_kwarg, page_number)
    def previous_page(self, page):
        if page.has_previous():
            #return '?{}={}'.format(self.page_kwargs, page.previous_page_number())
            return self._page_urls(page.previous_page_number())
        return None 
    def next_page(self, page):
        if page.has_next():
            return self._page_urls(page.next_page_number())
        return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #object_list = self.queryset
        tags = Tag.objects.all()
        paginator = Paginator(tags, self.paginated_by)
        page_number = self.request.GET.get('page_kwarg')
        #page = (context.get('page_obj'))
        #page = context.get('page_obj')
        page = paginator.get_page(page_number)
        #context['page_obj'] = page
        context['paginator'] = paginator
        context['tag_list'] = page
        #context['tag_list'] = page.object_list
        #context['is_paginated'] = True
        if page is not None:
            context.update({'next_page_url' : self.next_page(page), 'previous_page_url':self.previous_page(page)})
        return context
            
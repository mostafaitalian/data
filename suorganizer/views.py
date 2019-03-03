from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def redirect_view1(request):
    return HttpResponseRedirect('/blog/')

def redirect_view(request):
    return redirect('blog:blog_post_list')
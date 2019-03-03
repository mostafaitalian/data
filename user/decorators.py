from django.conf import settings
from django.contrib.auth import get_user
from django.shortcuts import redirect
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from scapy.contrib.skinny import cls
def custom_login_decorator(view):
    @wraps(view, assigned=available_attrs(view))
    def new_view(request,*args,**kwargs):
        
        user = get_user(request)
        user.is_authenticated
        if user.is_authenticated:
            return view(request,*args,**kwargs)
        else:
            url = '{}?next={}'.format(settings.LOGIN_URL, request.path)
            return redirect(url)
    return new_view

def custom_login_decorator2(view):
    
    login_decorator = login_required(view)
    return login_decorator

def class_login_decorator(cls):
    if not isinstance(cls, type) or not issubclass(cls, View):
        raise ImproperlyConfigured("you must login")
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls
def require_authenticated_permission(permission):
    
    def decorator(cls):
        if not isinstance(cls, type) or not issubclass(cls, View):
            raise ImproperlyConfigured('check permission and if you are login')
        check_auth = method_decorator(login_required)
        check_perm = method_decorator(permission_required(permission, raise_exception=True))
        cls.dispatch = check_auth(check_perm(cls.dispatch))
        return cls
    return decorator
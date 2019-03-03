from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from .forms import UserCreationForm, ProfileForm
from .utils import MailContextMixin, ProfileGetObjectMixin
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.contrib.messages import error
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes, smart_text
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.messages import success
from .models import Profile
from .decorators import class_login_decorator
class RegisterView(CreateView):
    template_name = "user/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('user:user_login')
'''    def post(self, request, *args, **kwargs):
        if request.method=='Post':
            form= self.form_class(request.post)
            if form.is_valid():
                user = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password'])
                user.save()
                return render(request, 'core/movie_list.html')
            else:
                return HttpResponse('something goes wrong')'''

class  UserLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        if request.user.is_alive():
            return HttpResponse("you can not login because you are already")
        else:
            return super().post(request, *args, **kwargs)
        
class CreateAccount(MailContextMixin, View):
    form_class = UserCreationForm
    template_name = 'user/user_create.html'
    success_url = reverse_lazy('user:user_create_done')
    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form':self.form_class()})
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save(**self.get_save_kwargs(request))
        if bound_form.mail_sent:
            return redirect(self.success_url)
        else:
            errs = bound_form.non_field_errors()
            for err in errs:
                error(request, err)
        return TemplateResponse(request, self.template_name, {'form':bound_form})
class ActivateAccount(MailContextMixin, View):
    template_name='user/user_activate.html'
    success_url = reverse_lazy('userr:user_login')
    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            #uid=urlsafe_base64_encode(force_text(request.user.pk)).decode()
            uid =force_text(urlsafe_base64_decode(uidb64), encoding='utf-8')
            user = User.objects.get(pk=uid)
        except (ValueError,TypeError, OverflowError, User.DoesNotExist):
            user = None
        if not user is None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            success(request, 'user is activated, you may login again')
            return redirect(self.success_url)
        else:
            return TemplateResponse(request, self.template_name)
@class_login_decorator       
class ProfileDetailView(ProfileGetObjectMixin, DetailView):
    model = Profile
class ProfileCreateView(CreateView):
    model = Profile
    form_class= ProfileForm    
class ProfileUpdateView(ProfileGetObjectMixin, UpdateView):
    model = Profile
    fields=('about',)
class PublicProfileUpdateView(ProfileGetObjectMixin, UpdateView):
    model=Profile
from django.urls import path, include
from django.conf.urls import url
from user.views import RegisterView, LoginView, CreateAccount,ActivateAccount, ProfileDetailView, ProfileUpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from user import views

app_name = 'user'
password_urls=[path('change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change_form.html', success_url=reverse_lazy('user:user_pw_change_done')),{'template_name':'user/password_change_form.html',
                                                                        'post_change_redirect': reverse_lazy('user:user_pw_change_done')}, name='user_pw_change'),
               path('change/done/',
                    auth_views.PasswordChangeDoneView.as_view(), name='user_pw_change_done'),
               path('reset/',
                    auth_views.PasswordResetView.as_view(template_name="user/password_reset_form.html",
                                                         from_email='mostafaitalian1379@gmail.com',
                                                         email_template_name='user/password_reset_email.txt',
                                                         html_email_template_name='user/password_reset_email.html',
                                                         subject_template_name="user/password_reset_subject.txt",
                                                         success_url=reverse_lazy('user:user_pw_reset_sent')),
                                                         name='user_pw_reset'),
               path('reset/sent/',
                    auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"),
                    name='user_pw_reset_sent'),
               path('reset/<uidb64>/<token>/',
                    auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', success_url=reverse_lazy('userr:user_pw_reset_complete')), name='user_pw_reset_confirm'),
               path('reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='user_pw_reset_complete')
               ]


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='userr:user_login', permanent=False)),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(),{'extra_context':{'form':AuthenticationForm}} , name='user_login' ),
    path('logout', auth_views.LogoutView.as_view(), name='user_logout'),
    path('password/', include(password_urls,)),
    path('change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change_form.html'),{'template_name':'user/password_change_form.html',
                                                             'post_change_redirect': reverse_lazy('user:user_pw_change_done')}, name='user_pw_change'),
    path('change/done/', auth_views.PasswordChangeDoneView.as_view(), name='user_pw_change_done'),
    path('create/', CreateAccount.as_view(), name='user_create'),
    path('create/done/', TemplateView.as_view(template_name='user/user_create_done.html'), name='user_create_done'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='user_activate'),
    path('profile/detail/', ProfileDetailView.as_view(), name='user_profile_detail'),
    path('profile/edit', ProfileUpdateView.as_view(), name='user_profile_update'),
    path('profile/<str:slug>/detail/', views.PublicProfileUpdateView.as_view(), name='user_profile_public_detail'),
    path('profile/create/', views.ProfileCreateView.as_view(), name="user_profile_create")
    ]
#[(u.username, u.email, u.is_active, u.has_usable_password()) for u in get_user_model().objects.all()]


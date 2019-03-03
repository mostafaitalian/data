from django.contrib.auth.signals import user_logged_in, user_logged_out

from django.contrib.messages import success

from django.dispatch import receiver
@receiver(user_logged_in)
def display_login_messagge(sender, **kwargs):
    request = kwargs.get('request')
    user = kwargs.get('user')
    success(request, 'you are successfully logged in..{}'.format(user.get_short_name()), fail_silently=True)
@receiver(user_logged_out)
def display_logout_message(sender, **kwargs):
    request = kwargs.get('request')
    message='you are successfully logged out--{}'
    success(request, message, fail_silently=True)
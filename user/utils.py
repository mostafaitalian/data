from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from smtplib import SMTPException
from django.core.mail.message import BadHeaderError
import traceback
import logging
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user
class ActivationMailFormMixin:
    mail_validation_error=''
    logger = logging.getLogger(__name__)
    def log_mail_error(self, **kwargs):
        msg_list = ['Activation email did not send.\n',
                    'from_email: {from_email}\n',
                    'subject: {subject}\n',
                    'message: {message}\n',]
        recipient_list = kwargs.get('recipient_list', [])
        for recipient in recipient_list:
            msg_list.insert(1, 'reciepient : {r}\n'.format(r=recipient))
        if 'error' in kwargs:
            level = 'ERROR'
            error_msg = ('error: {0.--class--.--name--}\n''args: {0.args}\n')
            error_info = error_msg.format(kwargs['error'])
            msg_list.insert(1, error_info)
        else:
            level = 'CRITICAL'
            msg = ''.join(msg_list).format(**kwargs)
            self.logger.log(level, msg)


    
    
    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False        
    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError('you can not set mail_sent property')
    
    def get_message(self, **kwargs):
        
        email_template_name = kwargs.get('email_template_name')
        context = kwargs.get('context')
        return render_to_string(email_template_name, context)
    
    def get_subject(self, **kwargs):
        subject_template_name=kwargs.get('subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(subject_template_name, context)
        #subject = ''.join(subject.splitlines())
        subject = 'subject'
        return subject
    def get_context_data(self, request, user, context=None):
        if context is None:
            context = dict()
        
        current_site = get_current_site(request)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        context.update({'domain' : current_site.domain,'protocol' : protocol, 'token' : token, 'uid' : str(uid), 'user' : user, 'site_name' : current_site.name})
        return context
    
    def _send_mail(self, request, user, **kwargs):
        kwargs['context'] = self.get_context_data(request, user)
        mail_kwargs = {
            'subject' : self.get_subject(**kwargs),
            'message' :self.get_message(**kwargs),
            'from_email' : 'mostafaitalian1379@gmail.com',
            'recipient_list' : (user.email,)
            }
        try:
            number_sent = send_mail(**mail_kwargs) 
        except Exception as error:
            self.log_mail_error(error=error, **mail_kwargs)
            if isinstance(error, BadHeaderError):
                err_code = 'badheader'
            elif isinstance(error, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpectederror'
            return (False, err_code)
        else:
            if number_sent>0:
                return (True, None)
        self.log_mail_error(**mail_kwargs)
        return (False, 'unknownerror')
    def send_mail(self, user, **kwargs):
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = [" " + line for line in tb]
            self.logger.warning('send_email called without request\ntraceback:\n{}'.format(''.join(tb)))
            self._mail_sent = False
            return self.mail_sent
        self._mail_sent, error = self._send_mail(request, user, **kwargs)
        if not self.mail_sent:
            return self.mail_sent
  
class MailContextMixin:
    email_template_name = 'user/email_create.txt'
    subject_template_name = 'user/subject_create.txt' 
    def get_save_kwargs(self, request):
        return {'email_template_name':self.email_template_name,
                'subject_template_name':self.subject_template_name,
                'request':request}
class ProfileGetObjectMixin:
    
    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile

        
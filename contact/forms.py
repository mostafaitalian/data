from django import forms
from django.core.mail import mail_managers, BadHeaderError
from django.core.exceptions import ValidationError
class ContactForm(forms.Form):
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    
    REASON_CHOICES = ((FEEDBACK, 'Feedback'),(CORRECTION, 'Correction'),(SUPPORT,'Support'))
    
    '''If we wanted to make the email field optional, we would set the required option to
False (the blank and null options are only for model fields).'''
    email = forms.EmailField(initial='youremail@domain.com')
    
    text = forms.CharField(widget = forms.Textarea) 
    
    reason = forms.ChoiceField(initial=FEEDBACK, choices=REASON_CHOICES)
    
    def send_email(self):
        reason = self.cleaned_data.get('reason')
        reason_dict = dict(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        body ='message from {}\n\n{}\n'.format(email, text)
        
        try:
            mail_managers(subject=full_reason, message = body)
        except BadHeaderError:
            self.add_error(None, ValidationError('email can not be sent due to big header', code='badheader'))
            return False
        else:
            return True
from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from django.contrib.messages import success
from django.contrib import messages
# Create your views here.
class ContactView(View):
    
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    
    def get(self, request):
        return render(request, self.template_name, {'form':self.form_class()})
    
    def post(self, request):
        
        form = self.form_class(request.POST)
        if form.is_valid():
        
            sent_email = form.send_email()
            if sent_email:
                messages.set_level(request, messages.SUCCESS)
                success(request, 'Email is successfuly sent')
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Email was not sent')
                return redirect('blog:blog_post_list')
        return render(request, self.template_name, {'form' : form })
                
    
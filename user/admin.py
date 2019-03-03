from django.contrib import admin
from .models import User
from .forms import UserCreationForm
# Register your models here.
#admin.site.register(User)
'''
admin.site.unregister(User)
admin.site.register(User, 'UserAdmin')'''
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form =UserCreationForm
    list_display = ('get_name', 'email', 'is_staff', 'is_superuser', 'get_joined_date')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'profile__joined')
    ordering = ('email',)
    list_display_links = ('get_name', 'email')
    
    # form view
    fieldsets = ((None, {'classes':('wide',),'fields': ('email',)}),
                 ('Permissions', {'classes':('collapse',),'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
                 ('Important dates', {'classes':('collapse',),'fields': ('last_login',)}),)
    filter_horizontal = ('groups', 'user_permissions')
    add_fieldsets = ((None,
                      {'classes': ('wide',),
                       'fields': ('name','email','password1','password2')}),)
    def get_name(self, user):
        return user.profile.name
    get_name.short_description='Name'
    
    def get_joined_date(self, user):
        return user.profile.joined
    get_joined_date.short_description = 'Joined'
    get_joined_date.admin_order_field = ('profile__joined')
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)
        
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
"""User django admin"""
#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#Models
from users.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ add profile admin to user  """
    #fields to show in model user
    list_display=('pk', 'user', 'role')
    # clickeable fields
    list_display_links = ('user','role')
    #readonly fields
    readonly_fields=('created','modified')

class ProfileInLine(admin.StackedInline):
    """ profile inline extend for users"""
    model=Profile
    can_delete=False
    verbose_name_plural ='profiles'
class UserAdmin(BaseUserAdmin):
    inlines=(ProfileInLine,)
    
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

    
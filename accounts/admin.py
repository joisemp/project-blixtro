from django.contrib import admin
from . models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_admin', 'is_staff')
    
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (_('User'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_admin', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    search_fields = ('email', 'first_name', 'last_name')

from django.contrib import admin
from . models import User, UserProfile, Org, Department
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff')
    
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (_('User'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    search_fields = ('email',)
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


admin.site.register(Org)
admin.site.register(Department)
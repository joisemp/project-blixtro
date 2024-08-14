from django.contrib import admin
from .models import Lab, Category, Item, System, SystemComponent, Brand

admin.site.register(Category)
admin.site.register(Brand)


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('org', 'dept', 'lab_name')
    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'item_name', 'total_qty')
    
    
@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'lab', 'sys_name')
    

@admin.register(SystemComponent)
class SystemComponentAdmin(admin.ModelAdmin):
    list_display = ('system', 'item', 'component_type')
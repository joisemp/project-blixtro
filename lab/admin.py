from django.contrib import admin
from .models import Lab, Category, Item, ItemGroup

admin.site.register(Lab)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemGroup)

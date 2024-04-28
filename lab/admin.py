from django.contrib import admin
from .models import Lab, Category, Item, Group, GroupItem

admin.site.register(Lab)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Group)
admin.site.register(GroupItem)

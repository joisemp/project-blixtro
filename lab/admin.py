from django.contrib import admin
from .models import Lab, Label, Category, Item

admin.site.register(Lab)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(Item)

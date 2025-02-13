from django.contrib import admin
from inventory.models import *

admin.site.register(Department)
admin.site.register(Rooms)
admin.site.register(Activity)
admin.site.register(Vendors)
admin.site.register(Purchase)


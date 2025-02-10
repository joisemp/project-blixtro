from django.urls import path
from inventory.views import central_admin

app_name = 'central_admin'

urlpatterns = [
    path('', central_admin.DashboardView.as_view(), name='admin-dashboard'),
]

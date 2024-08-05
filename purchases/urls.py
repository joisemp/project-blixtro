from django.urls import path
from purchases import views

app_name = 'purchases'

urlpatterns = [
    #bpath('labs/', views.LabListView.as_view(), name='lab-list'),
    path('', views.PurchaseListView.as_view(), name='purchase-list')
]


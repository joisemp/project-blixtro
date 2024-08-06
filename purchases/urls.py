from django.urls import path
from purchases import views

app_name = 'purchases'

urlpatterns = [
    path('', views.PurchaseListView.as_view(), name='purchase-list'),
    path('create/', views.PurchaseCreateView.as_view(), name='create-purchase'),
]


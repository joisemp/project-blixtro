from django.urls import path
from purchases import views

app_name = 'purchases'

urlpatterns = [
    path('', views.PurchaseListView.as_view(), name='purchase-list'),
    path('create/', views.PurchaseCreateView.as_view(), name='create-purchase'),
    path('<int:purchase_id>/', views.PurchaseDetailView.as_view(), name='purchase-detail'),
    path('<int:purchase_id>/update/', views.PurchaseUpdateView.as_view(), name='purchase-update'),
    path('<int:purchase_id>/delete/', views.PurchaseDeleteView.as_view(), name='purchase-delete'),
]


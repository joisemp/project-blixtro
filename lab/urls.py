from django.urls import path
from .import views

app_name = 'lab'

urlpatterns = [
    path('', views.LabListView.as_view(), name='lab-list'),
    path('create/', views.LabCreateView.as_view(), name='lab-create'),
    path('<int:pk>/update/', views.UpdateLabView.as_view(), name='lab-update'),
    path('<int:pk>/delete/', views.DeleteLabView.as_view(), name='lab-delete'),
    
    path('<int:pk>/items/add-item/', views.CreateItemView.as_view(), name='add-item'),
    path('<int:pk>/items/', views.ItemListView.as_view(), name='item-list'),
    path('<int:pk>/items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('<int:pk>/items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    
    path('<int:pk>/groups/create/', views.ItemGroupCreateView.as_view(), name='create-group'),
    path('<int:pk>/groups/', views.ItemGroupListView.as_view(), name='group-list'),
    path('<int:pk>/groups/<int:itemgroup>/', views.ItemGroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/groups/<int:itemgroup>/delete/', views.ItemGroupDeleteView.as_view(), name='group-delete'),
]
from django.urls import path
from . import views
from core.views import LabStaffCreateView

app_name = 'lab'

urlpatterns = [
    path('labs/', views.LabListView.as_view(), name='lab-list'),
    path('labs/create/', views.LabCreateView.as_view(), name='lab-create'),
    path('labs/create/add-user/', LabStaffCreateView.as_view(), name='lab-staff-create'),
    path('labs/<int:lab_id>/update/', views.UpdateLabView.as_view(), name='lab-update'),
    path('labs/<int:lab_id>/delete/', views.DeleteLabView.as_view(), name='lab-delete'),
    
    path('labs/<int:lab_id>/items/add-item/', views.CreateItemView.as_view(), name='add-item'),
    path('labs/<int:lab_id>/items/', views.ItemListView.as_view(), name='item-list'),
    path('labs/<int:lab_id>/items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('labs/<int:lab_id>/items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    
    path('labs/<int:lab_id>/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('labs/<int:lab_id>/categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('labs/<int:lab_id>/categories/delete/<int:category>/', views.CategoryDeleteView.as_view(), name='category-delete'),
]


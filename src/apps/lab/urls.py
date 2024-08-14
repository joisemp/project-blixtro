from django.urls import path, include
from . import views
from apps.core.views import LabStaffCreateView

app_name = 'lab'

urlpatterns = [
    path('', views.LabListView.as_view(), name='lab-list'),
    path('create/', views.LabCreateView.as_view(), name='lab-create'),
    path('create/add-user/', LabStaffCreateView.as_view(), name='lab-staff-create'),
    path('<int:lab_id>/update/', views.UpdateLabView.as_view(), name='lab-update'),
    path('<int:lab_id>/delete/', views.DeleteLabView.as_view(), name='lab-delete'),
    path('<int:lab_id>/settings/', views.LabSettingsView.as_view(), name='lab-settings'),
    # path('<int:lab_id>/generate-report/', GenerateLabReportView.as_view(), name='generate-lab-report'),
    
    path('<int:lab_id>/items/add-item/', views.CreateItemView.as_view(), name='add-item'),
    path('<int:lab_id>/items/', views.ItemListView.as_view(), name='item-list'),
    # path('<int:lab_id>/items/generate-report/', GenerateLabItemReportView.as_view(), name='item-report'),
    path('<int:lab_id>/items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('<int:lab_id>/items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    path('<int:lab_id>/items/<int:item_id>/remove/', views.RecordItemRemovalView.as_view(), name='item-remove'),
    
    path('<int:lab_id>/systems/add-system/', views.SystemCreateView.as_view(), name='add-system'),
    path('<int:lab_id>/systems/', views.SystemListView.as_view(), name='system-list'),
    path('<int:lab_id>/systems/<int:sys_id>/', views.SystemDetailView.as_view(), name='system-detail'),
    path('<int:lab_id>/systems/<int:sys_id>/load_items/', views.LoadItemsView.as_view(), name='load_items'),
    path('<int:lab_id>/systems/<int:sys_id>/add-system-component/', views.SystemComponentCreateView.as_view(), name='add_component'),
    path('<int:lab_id>/systems/<int:sys_id>/delete-system-component/<int:component_id>/', views.SystemComponentDeleteView.as_view(), name='delete_component'),
    # path('<int:lab_id>/systems/generate-report/', GenerateLabSystemReportView.as_view(), name='system-report'),
    path('<int:lab_id>/systems/<int:sys_id>/update/', views.SystemUpdateView.as_view(), name='update-system'),
    path('<int:lab_id>/systems/<int:sys_id>/delete/', views.SystemDeleteView.as_view(), name='system-delete'),
    
    path('<int:lab_id>/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('<int:lab_id>/categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('<int:lab_id>/categories/delete/<int:category>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    path('<int:lab_id>/brands/', views.BrandListView.as_view(), name='brand-list'),
    path('<int:lab_id>/brands/create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('<int:lab_id>/brands/delete/<int:brand>/', views.BrandDeleteView.as_view(), name='brand-delete'),
    
    path('<int:lab_id>/purchases/', include('apps.purchases.urls', namespace='purchases')),
]


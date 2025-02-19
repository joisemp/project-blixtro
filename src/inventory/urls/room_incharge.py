from django.urls import path
from inventory.views import room_incharge

app_name = 'room_incharge'

urlpatterns = [
    path('rooms/<slug:room_slug>/categories/', room_incharge.CategoryListView.as_view(), name='category_list'),
    path('rooms/<slug:room_slug>/categories/<slug:category_slug>/update/', room_incharge.CategoryUpdateView.as_view(), name='category_update'),
    path('rooms/<slug:room_slug>/categories/<slug:category_slug>/delete/', room_incharge.CategoryDeleteView.as_view(), name='category_delete'),
    path('rooms/<slug:room_slug>/categories/create/', room_incharge.CategoryCreateView.as_view(), name='category_create'),
    path('rooms/<slug:room_slug>/brands/', room_incharge.BrandListView.as_view(), name='brand_list'),
    path('rooms/<slug:room_slug>/brands/create/', room_incharge.BrandCreateView.as_view(), name='brand_create'),
    path('rooms/<slug:room_slug>/brands/<slug:brand_slug>/update/', room_incharge.BrandUpdateView.as_view(), name='brand_update'),
    path('rooms/<slug:room_slug>/brands/<slug:brand_slug>/delete/', room_incharge.BrandDeleteView.as_view(), name='brand_delete'),
    path('rooms/<slug:room_slug>/items/', room_incharge.ItemListView.as_view(), name='item_list'),
    path('rooms/<slug:room_slug>/items/create/', room_incharge.ItemCreateView.as_view(), name='item_create'),
    path('rooms/<slug:room_slug>/items/<slug:item_slug>/update/', room_incharge.ItemUpdateView.as_view(), name='item_update'),
    path('rooms/<slug:room_slug>/items/<slug:item_slug>/delete/', room_incharge.ItemDeleteView.as_view(), name='item_delete'),
    path('rooms/<slug:room_slug>/items/<slug:item_slug>/archive/', room_incharge.ItemArchiveView.as_view(), name='item_archive'),
    path('rooms/<slug:room_slug>/systems/', room_incharge.SystemListView.as_view(), name='system_list'),
    path('rooms/<slug:room_slug>/systems/create/', room_incharge.SystemCreateView.as_view(), name='system_create'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/update/', room_incharge.SystemUpdateView.as_view(), name='system_update'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/delete/', room_incharge.SystemDeleteView.as_view(), name='system_delete'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/components/', room_incharge.SystemComponentListView.as_view(), name='system_component_list'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/components/create/', room_incharge.SystemComponentCreateView.as_view(), name='system_component_create'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/components/<slug:component_slug>/update/', room_incharge.SystemComponentUpdateView.as_view(), name='system_component_update'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/components/<slug:component_slug>/delete/', room_incharge.SystemComponentDeleteView.as_view(), name='system_component_delete'),
    path('rooms/<slug:room_slug>/systems/<slug:system_slug>/components/<slug:component_slug>/archive/', room_incharge.SystemComponentArchiveView.as_view(), name='system_component_archive'),
    path('rooms/<slug:room_slug>/archives/', room_incharge.ArchiveListView.as_view(), name='archive_list'),
    path('rooms/<slug:room_slug>/dashboard/', room_incharge.RoomDashboardView.as_view(), name='room_dashboard'),
]
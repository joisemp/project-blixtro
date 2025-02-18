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
    path('rooms/<slug:room_slug>/dashboard/', room_incharge.RoomDashboardView.as_view(), name='room_dashboard'),
]
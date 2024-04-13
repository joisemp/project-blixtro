from django.urls import path
from .import views

app_name = 'lab'

urlpatterns = [
    path('', views.LabListView.as_view(), name='lab-list'),
    path('create/', views.LabCreateView.as_view(), name='lab-create'),
    path('<int:pk>/', views.LabDetailView.as_view(), name='lab-detail'),
    path('<int:pk>/update/', views.UpdateLabView.as_view(), name='lab-update'),
    path('<int:pk>/delete/', views.DeleteLabView.as_view(), name='lab-delete'),
    path('<int:pk>/<int:itemgroup_id>/add-item/', views.CreateItemView.as_view(), name='add-item'),
    path('<int:pk>/<int:itemgroup_id>/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('<int:pk>/create-group/', views.ItemGroupCreateView.as_view(), name='create-group'),
    path('<int:pk>/<int:itemgroup_id>/', views.ItemGroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/<int:itemgroup_id>/delete/', views.ItemGroupDeleteView.as_view(), name='group-delete'),
]
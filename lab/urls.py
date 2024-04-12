from django.urls import path
from .import views

app_name = 'lab'

urlpatterns = [
    path('', views.LabListView.as_view(), name='lab-list'),
    path('create/', views.LabCreateView.as_view(), name='lab-create'),
    path('<int:pk>/', views.LabDetailView.as_view(), name='lab-detail'),
    path('<int:pk>/update/', views.UpdateLabView.as_view(), name='lab-update'),
    path('<int:pk>/delete/', views.DeleteLabView.as_view(), name='lab-delete'),
    path('<int:pk>/add-item/', views.AddItemView.as_view(), name='add-item'),
    path('<int:pk>/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item-update'),
]
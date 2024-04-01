from django.urls import path
from .import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
]
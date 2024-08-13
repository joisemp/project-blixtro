from django.urls import path, include
from org import views
from core import views as core_views

app_name = 'org'

urlpatterns = [
    path('<int:org_id>/', views.OrgDetailView.as_view(), name='org-dashboard'),
    path('<int:org_id>/people/', views.OrgPeopleListView.as_view(), name='org-people-list'),
    path('<int:org_id>/dept/create/', views.DepartmentCreateView.as_view(), name='dept-create'),
    # path('<int:org_id>/generate-report/', core_views.GenerateReportView.as_view(), name='generate-report'),
    
    path('<int:org_id>/dept/<int:dept_id>/lab/', include('lab.urls', namespace='lab')),
]


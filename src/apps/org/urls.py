from django.urls import path, include
from apps.org import views

app_name = 'org'

urlpatterns = [
    path('<int:org_id>/depts/', views.OrgDetailView.as_view(), name='org-dashboard'),
    path('<int:org_id>/people/', views.OrgPeopleListView.as_view(), name='org-people-list'),
    path('<int:org_id>/depts/create/', views.DepartmentCreateView.as_view(), name='dept-create'),
    path('<int:org_id>/depts/<int:dept_id>/update/', views.DepartmentUpdateView.as_view(), name='dept-update'),
    # path('<int:org_id>/generate-report/', core_views.GenerateReportView.as_view(), name='generate-report'),
    
    path('<int:org_id>/depts/<int:dept_id>/lab/', include('apps.lab.urls', namespace='lab')),
]


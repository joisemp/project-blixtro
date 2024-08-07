from django.urls import path
from core import views as core_views

app_name = 'org'

urlpatterns = [
    path('<int:org_id>/', core_views.OrgDetailView.as_view(), name='org-dashboard'),
    path('<int:org_id>/generate-report/', core_views.GenerateReportView.as_view(), name='generate-report'),
    path('<int:org_id>/people/', core_views.OrgPeopleListView.as_view(), name='org-people-list'),
    path('<int:org_id>/dept/create/', core_views.DepartmentCreateView.as_view(), name='dept-create'),
    path('<int:org_id>/dept/create/add-user/', core_views.DeptIncargeCreateView.as_view(), name='dept-incharge-create'),
]


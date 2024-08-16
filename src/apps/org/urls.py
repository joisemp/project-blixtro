from django.urls import path, include
from apps.org import views
from apps.purchases import views as purchase_views

app_name = 'org'

urlpatterns = [
    path('<int:org_id>/depts/', views.DepartmentListView.as_view(), name='dept-list'),
    path('<int:org_id>/people/', views.OrgPeopleListView.as_view(), name='org-people-list'),
    path('<int:org_id>/depts/create/', views.DepartmentCreateView.as_view(), name='dept-create'),
    path('<int:org_id>/depts/<int:dept_id>/update/', views.DepartmentUpdateView.as_view(), name='dept-update'),
    path('<int:org_id>/depts/<int:dept_id>/delete/', views.DepartmentDeleteView.as_view(), name='dept-delete'),
    # path('<int:org_id>/generate-report/', core_views.GenerateReportView.as_view(), name='generate-report'),
    
    path('<int:org_id>/vendors/add/', purchase_views.VendorCreateView.as_view(), name='vendor-create'),
    path('<int:org_id>/vendors/', views.AdminVendorsListView.as_view(), name='vendors-list'),
    path('<int:org_id>/vendors/<int:vendor_id>/delete', purchase_views.VendorDeleteView.as_view(), name='vendor-delete'),
    
    path('<int:org_id>/depts/<int:dept_id>/lab/', include('apps.lab.urls', namespace='lab')),
]


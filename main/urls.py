from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import LandingPageView, OrgDetailView, DepartmentCreateView, DeptIncargeCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('core/', include('core.urls', namespace='core')),
    path('org/<int:org_id>/', OrgDetailView.as_view(), name='org-dashboard'),
    path('org/<int:org_id>/dept/create/', DepartmentCreateView.as_view(), name='dept-create'),
    path('org/<int:org_id>/dept/create/add-user/', DeptIncargeCreateView.as_view(), name='dept-incharge-create'),
    path('org/<int:org_id>/dept/<int:dept_id>/', include('lab.urls', namespace='lab')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.urls import path
from inventory.views import central_admin

app_name = 'central_admin'

urlpatterns = [
    path('', central_admin.DashboardView.as_view(), name='dashboard'),
    path('people/', central_admin.PeopleListView.as_view(), name='people_list'),
    path('people/create/', central_admin.PeopleCreateView.as_view(), name='people_create'),
    path('rooms/', central_admin.RoomListView.as_view(), name='room_list'),
    path('vendors/', central_admin.VendorListView.as_view(), name='vendor_list'),
    path('purchases/', central_admin.PurchaseListView.as_view(), name='purchase_list'),
    path('issues/', central_admin.IssueListView.as_view(), name='issue_list'),
]

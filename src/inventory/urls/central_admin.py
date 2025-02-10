from django.urls import path
from inventory.views import central_admin

app_name = 'central_admin'

urlpatterns = [
    path('', central_admin.DashboardView.as_view(), name='dashboard'),
    path('people_list/', central_admin.PeopleListView.as_view(), name='people_list'),
    path('room_list/', central_admin.RoomListView.as_view(), name='room_list'),
    path('vendor_list/', central_admin.VendorListView.as_view(), name='vendor_list'),
    path('purchase_list/', central_admin.PurchaseListView.as_view(), name='purchase_list'),
    path('issue_list/', central_admin.IssueListView.as_view(), name='issue_list'),
]

from django import forms
from inventory.models import Department,Rooms

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['department_name']


class RoomForm(forms.ModelForm):

    class Meata:
        model = Rooms
        fields = ['label','room_name','incharge']


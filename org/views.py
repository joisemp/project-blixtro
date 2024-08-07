from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from purchases.models import Org, Department
from core.models import UserProfile


class OrgDetailView(generic.DetailView):
    template_name = 'core/org-dashboard.html'
    model = Org
    
    def get_object(self, queryset=None):
        org_id = self.kwargs['org_id']
        queryset = self.get_queryset()
        return queryset.get(pk=org_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        context["departments"] = Department.objects.filter(org=org)
        return context


class DepartmentCreateView(generic.CreateView):
    template_name = "core/dept-create.html"
    model = Department
    fields = ["name", "head"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_id"] = self.kwargs["org_id"]
        return context
    
    def form_valid(self, form):
        dept = form.save(commit=False)
        org = self.request.user.profile.org
        dept.org = org
        dept.save()
        department_head = dept.head
        department_head.dept = dept
        department_head.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["head"].queryset = UserProfile.objects.filter(is_dept_incharge=True, org=self.request.user.profile.org)
        return form
    
    def get_success_url(self):
        org_id = self.kwargs['org_id']
        return reverse('org:org-dashboard', kwargs={'org_id':org_id})


class OrgPeopleListView(generic.ListView):
    model = UserProfile
    template_name = 'core/org-people-list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Org.objects.get(pk = self.kwargs["org_id"])
        org_people = UserProfile.objects.filter(org=org)
        context["org_people"] = org_people
        context["org"] = org
        return context


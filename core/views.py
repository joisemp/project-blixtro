from django.urls import reverse, reverse_lazy
from . utils import generate_password
from . forms import CustomAuthenticationForm, CustomOrgRegisterForm
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect
from . models import User, Org, UserProfile, Department
from .account_activation_email import send_account_activation_mail
from . token_generator import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_str
from . forms import LabStaffCreationForm
from lab.mixins import AdminOnlyAccessMixin, RedirectLoggedInUserMixin


class LandingPageView(RedirectLoggedInUserMixin, generic.TemplateView):
    template_name = 'landing_page.html'


class UserRegisterView(generic.CreateView):
    form_class = CustomOrgRegisterForm
    template_name = 'core/register-user.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        org_name = form.cleaned_data.get('org_name')
        org_address = form.cleaned_data.get('org_address')
        org_email = form.cleaned_data.get('org_email')
        org_website_url = form.cleaned_data.get('org_website_url')
        
        org = Org.objects.create(
            org_name=org_name,
            contact = org_email,
            website_url = org_website_url,
            address = org_address
        )
        
        UserProfile.objects.create(
            user = user,
            org = org,
            first_name = first_name,
            last_name = last_name,
            is_org_admin = True
        )
        
        send_account_activation_mail(self.request, user, email = user.email)
        return super(UserRegisterView, self).form_valid(form)  
    
    def get_success_url(self):
        return reverse('core:login')  


class LoginView(views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('landing-page')
    
    
class LogoutView(views.LogoutView):
    template_name = 'core/logout.html'


class ChangePasswordView(views.PasswordChangeView):
    template_name = 'core/change-password.html'
    success_url = reverse_lazy('landing-page')


class ResetPasswordView(views.PasswordResetView):
    email_template_name = 'core/password_reset/password_reset_email.html'
    html_email_template_name = 'core/password_reset/password_reset_email.html'
    subject_template_name = 'core/password_reset/password_reset_subject.txt'
    success_url = reverse_lazy('core:done-password-reset')
    template_name = 'core/password_reset/password_reset_form.html'


class DonePasswordResetView(views.PasswordResetDoneView):
    template_name = 'core/password_reset/password_reset_done.html'


class ConfirmPasswordResetView(views.PasswordResetConfirmView):
    success_url = reverse_lazy('core:complete-password-reset')
    template_name = 'core/password_reset/password_reset_confirm.html'


class CompletePasswordResetView(views.PasswordResetCompleteView):
    template_name = 'core/password_reset/password_reset_complete.html'

""" 
class AddUserView(generic.CreateView):
    fields = ['email', 'first_name', 'last_name']
    model = User
    template_name = 'core/add-user-form.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = str(generate_password())
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        
        user = User.objects.create(
            email=email,
            password=password,
        )
        
        return redirect('lab:lab-list')
"""

class LabStaffCreateView(generic.FormView):
    model = User
    template_name = 'core/lab-staff-create.html'
    form_class = LabStaffCreationForm
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = str(generate_password())
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        
        user = User.objects.create(
            email=email,
            password=password,
        )
        
        user_profile = UserProfile.objects.create(
            first_name = first_name,
            last_name = last_name,
            user = user,
            org = org,
            is_lab_staff = True
        )
        
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:lab-create', kwargs={'org_id':org_id, 'dept_id':dept_id})
    

class DeptIncargeCreateView(generic.FormView):
    model = User
    form_class = LabStaffCreationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_id"] = self.kwargs["org_id"]
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = str(generate_password())
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        org = Org.objects.get(pk=self.kwargs["org_id"])
        
        user = User.objects.create(
            email=email,
            password=password,
        )
        
        UserProfile.objects.create(
            first_name = first_name,
            last_name = last_name,
            user = user,
            org = org,
            is_dept_incharge = True
        )
        
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        return reverse('dept-create', kwargs={'org_id':org_id})
    

class ActivateAccountView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


class OrgDetailView(AdminOnlyAccessMixin, generic.DetailView):
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
    fields = ["name", "incharge"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_id"] = self.kwargs["org_id"]
        return context
    
    def form_valid(self, form):
        dept = form.save(commit=False)
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        dept.org = org
        dept.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        form.fields['incharge'].queryset = UserProfile.objects.filter(org=org, is_dept_incharge=True)
        return form
    
    def get_success_url(self):
        org_id = self.kwargs['org_id']
        return reverse('org-dashboard', kwargs={'org_id':org_id})


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
    
    
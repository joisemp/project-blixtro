from django.urls import reverse, reverse_lazy

from lab.models import Item, Lab
from core.utils import generate_password, get_lab_item_report_data, get_lab_report_data, get_lab_system_report_data, get_report_data 
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect
from core.models import User, UserProfile
from org.models import Org, Department
from core.account_activation_email import send_account_activation_mail
from core.token_generator import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.encoding import force_str
from core.forms import LabStaffCreationForm, CustomAuthenticationForm, CustomOrgRegisterForm
from lab.mixins import AdminOnlyAccessMixin, RedirectLoggedInUserMixin

from django.template.loader import render_to_string
from xhtml2pdf import pisa



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
    fields = ["name"]
    
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
    
    
class GenerateReportView(generic.View):
    def get(self, request, org_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        userprofile = UserProfile.objects.get(user=request.user)
        org = userprofile.org
        
        report = get_report_data(org)
        
        print(report)

        # Combine report data
        report_data = {
            'organization_name': org.org_name,
            'lab_count':len(report),
            'lab_report': report
        }
        

        # Render HTML template
        template_name = 'core/report.html'  # Replace with your actual template name
        html = render_to_string(template_name, report_data)

        # Configure xhtml2pdf options (optional)
        pdf_options = {
            'page-size': 'A4',  # Set desired page size
            'encoding': 'utf-8',  # Set encoding for text content
        }

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

        result = pisa.CreatePDF(html, dest=response, options=pdf_options)
        if result.err:
            return HttpResponse('Error: {}'.format(result.err))  # Handle errors

        return response
    
    
    
class GenerateLabReportView(generic.View):
    def get(self, request, org_id, dept_id, lab_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        userprofile = UserProfile.objects.get(user=request.user)
        org = userprofile.org
        lab = Lab.objects.get(pk = lab_id)
        
        report = get_lab_report_data(lab)
        

        # Combine report data
        report_data = {
            'organization_name': org.org_name,
            'lab': report
        }
        

        # Render HTML template
        template_name = 'core/lab-report.html'  # Replace with your actual template name
        html = render_to_string(template_name, report_data)

        # Configure xhtml2pdf options (optional)
        pdf_options = {
            'page-size': 'A4',  # Set desired page size
            'encoding': 'utf-8',  # Set encoding for text content
        }

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

        result = pisa.CreatePDF(html, dest=response, options=pdf_options)
        if result.err:
            return HttpResponse('Error: {}'.format(result.err))  # Handle errors

        return response
    
    
class GenerateLabItemReportView(generic.View):
    def get(self, request, org_id, dept_id, lab_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        userprofile = UserProfile.objects.get(user=request.user)
        org = userprofile.org
        lab = Lab.objects.get(pk = lab_id)
        
        report = get_lab_item_report_data(lab)
        

        # Combine report data
        report_data = {
            'organization_name': org.org_name,
            'lab': report
        }
        

        # Render HTML template
        template_name = 'core/lab-report.html'  # Replace with your actual template name
        html = render_to_string(template_name, report_data)

        # Configure xhtml2pdf options (optional)
        pdf_options = {
            'page-size': 'A4',  # Set desired page size
            'encoding': 'utf-8',  # Set encoding for text content
        }

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

        result = pisa.CreatePDF(html, dest=response, options=pdf_options)
        if result.err:
            return HttpResponse('Error: {}'.format(result.err))  # Handle errors

        return response
    

class GenerateLabSystemReportView(generic.View):
    def get(self, request, org_id, dept_id, lab_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        userprofile = UserProfile.objects.get(user=request.user)
        org = userprofile.org
        lab = Lab.objects.get(pk = lab_id)
        
        report = get_lab_system_report_data(lab)
        

        # Combine report data
        report_data = {
            'organization_name': org.org_name,
            'lab': report
        }
        

        # Render HTML template
        template_name = 'core/lab-report.html'  # Replace with your actual template name
        html = render_to_string(template_name, report_data)

        # Configure xhtml2pdf options (optional)
        pdf_options = {
            'page-size': 'A4',  # Set desired page size
            'encoding': 'utf-8',  # Set encoding for text content
        }

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

        result = pisa.CreatePDF(html, dest=response, options=pdf_options)
        if result.err:
            return HttpResponse('Error: {}'.format(result.err))  # Handle errors

        return response
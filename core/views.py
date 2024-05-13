from django.urls import reverse, reverse_lazy
from . utils import generate_password
from . forms import CustomAuthenticationForm, CustomOrgRegisterForm
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect
from . models import User, Org, UserProfile
from .account_activation_email import send_account_activation_mail
from . token_generator import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_str


class LandingPageView(generic.TemplateView):
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
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        return redirect('lab:lab-list')
          

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


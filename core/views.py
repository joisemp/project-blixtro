from . forms import CustomAuthenticationForm
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect

class LandingPageView(generic.TemplateView):
    template_name = 'landing_page.html'
    

class LoginView(views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return redirect('landing-page')
    
class LogoutView(views.LogoutView):
    template_name = 'core/logout.html'

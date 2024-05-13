from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True}))
    

class CustomOrgRegisterForm(UserCreationForm):
    org_name = forms.CharField(
        widget=forms.TextInput(attrs={'required':True}),
        label='Organisation Name'
    )
    
    org_address = forms.CharField(
        widget=forms.Textarea(attrs={'required':True, 'rows':5}),
        label='Organisation Address'
    )
    
    org_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'required':True}),
        label='Organisation Email'
    )
    
    org_website_url = forms.CharField(
        widget=forms.TextInput(attrs={'required':True}),
        label='Organisation Website'
    )
    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'required':True}),
        label='First Name'
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'required':True}),
        label='Last Name'
    )
    
    field_order = [
        'org_name',
        'org_address',
        'org_email',
        'org_website_url',
        'first_name', 
        'last_name', 
        'email', 
        'password1', 
        'password2'
    ]
    
    class Meta:
        model = User
        fields = ['email']
        
        
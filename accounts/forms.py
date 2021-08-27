from django import forms
from accounts.models import Account
from django.core.exceptions import ValidationError
from django.contrib import messages

class RegistrationForm(forms.ModelForm):
    email           = forms.EmailField(required=True)
    confirm_email   = forms.EmailField(required=True)
    confirm_password= forms.CharField(required=True,widget=forms.PasswordInput())
    class Meta:
        model=Account
        fields=['first_name', 'last_name','username','email','confirm_email','password','confirm_password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        self.fields['first_name'].widget.attrs['placeholder']='Geben Sie Ihr Name ein :'

    def clean(self):
        cleaned_data         =super(RegistrationForm,self).clean()
        email                = cleaned_data.get('email')
        confirm_email        = cleaned_data.get('confirm_email')
        password             = cleaned_data.get('password')
        confirm_password     = cleaned_data.get('confirm_password')
        if email != confirm_email:
            raise forms.ValidationError('Die eingegebene Emails sind nicht gleich!')
        if password != password:
            raise forms.ValidationError('Die eingegebene passwords sind nicth gleich')
class LoginForm(forms.Form):
    email               = forms.EmailField(required=True)
    password            = forms.CharField(required=True,widget=forms.PasswordInput())

class ResetpassEmailForm(forms.Form):
    email                = forms.EmailField(required=True)
    def __init__(self,*args,**kwargs):
        super(ResetpassEmailForm,self).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder']='Geben Sie Ihr Email Add ein'

class ChangePasswordForm(forms.Form):
        password                = forms.CharField(required=True,widget=forms.PasswordInput())
        confirm_password        = forms.CharField(required=True,widget=forms.PasswordInput())
        def clean(self):
            cleaned_data        = super(ChangePasswordForm,self).clean()
            password            = cleaned_data.get('password')
            confirm_password    = cleaned_data.get('confirm_password')
            if confirm_password != password:
                raise forms.ValidationError('Password sind nicht gleich!')
            

from django.shortcuts import render
from django.views.generic import FormView,ListView
from accounts.forms import RegistrationForm,LoginForm,ResetpassEmailForm,ChangePasswordForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect,Http404
from accounts.models import Account,ResetPassword
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from carts.models import Cart,CartItem
# Email Activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError




# Create your views here.



class RegisterView(FormView):
    template_name='shopapp/register.html'
    form_class=RegistrationForm
    success_url = '/accounts/login/'
    def form_valid(self,form):
        user=form.save()
        if user:
            user.set_password(user.password)
            user.is_admin=True
            user.active  = True
            user.save()
            messages.success(self.request,'Ihre Account wurde erfolgreich hizugefugt! Bitte Actieriern ihre account')
# USER Activation
            mail_subject  ='Bitte activieren ihre Konto'
            message       = render_to_string('shopapp/account_verification_email.html',{
            'user'        : user,
            'domain'      : get_current_site,
            'uid'         : urlsafe_base64_encode(force_bytes(user.id)),
            'token'       : default_token_generator.make_token(user)
            })
            to_email      = user.email
            send_email    = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
        return super().form_valid(form)



class Login(FormView):
    template_name='shopapp/signin.html'
    form_class=LoginForm
    success_url = '/accounts/'
    def form_valid(self,form):
        email        = self.request.POST['email']
        password     = self.request.POST['password']
        user         = authenticate(email=email,password=password)
        if user:
            if user.is_active:
                login(self.request, user)
                if user.is_superadmin or user.is_staff:
                    messages.success(self.request,'{user} Successfully signed'.format(user=user))
                    return HttpResponseRedirect('admin')
                messages.success(self.request,'  Welcomen {user}'.format(user=user))
                return HttpResponseRedirect(reverse('accounts:dashboard'))
            else:
                messages.error(self.request,'  your account is not active')
                return HttpResponseRedirect(reverse('accounts:login'))
        else:
            messages.error(self.request,' Sie mussen zuerst ihre konto activieren')
            return HttpResponseRedirect(reverse('accounts:login'))


def activate(request,uidb64,token):
    try:
        uid              = urlsafe_base64_decode(uidb64).decode()
        user             = Account.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user             = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active   = True
        user.save()
        messages.success(request, "Herzlich willkommen ihre Email Address is jetz active")
        return HttpResponseRedirect(reverse('accounts:login'))
    else:
        messages.success(request, "Invalid Link")
        return HttpResponseRedirect(reverse('accounts:register'))
class DashboardView(ListView):
    template_name           = "shopapp/dashboard.html"
    model                   = CartItem
class Resetpass(FormView):
    form_class     = ResetpassEmailForm
    template_name  = 'shopapp/forgetpass.html'
    success_url    = '/accounts/resetpass/'
    def form_valid(self,form):
        email         = form.cleaned_data['email']
        try:
            user          = Account.objects.get(email=email)
            mail_subject  = 'Reset password Email'
            mail_to       = user.email
            token         = default_token_generator.make_token(user)
            uid           = urlsafe_base64_encode(force_bytes(user.id))
            domain        = get_current_site(self.request)
            email_body    = render_to_string('shopapp/reset_password.html',{
                          'uid'    : uid,
                          'token'  : token,
                          'domain' : domain,
                          'user'   : user,
            })
            send_email        = EmailMessage(mail_subject,email_body,to=[mail_to])
            if send_email.send():
                db=ResetPassword.objects.create(uidb64=uid,token=token)
                db.save()
                messages.success(self.request,'reset password link wurde an {email} geschickt.'.format(email=mail_to))
                return super().form_valid(form)
            else:
                messages.error(self.request,'Etwas Schief gelaufen .....')
                return HttpResponseRedirect(reverse('accounts:resetpass'))
        except (KeyError,TypeError,OverflowError,ValueError,Account.DoesNotExist):
            messages.error(self.request,'Etwas Schief gelaufen .....')
            return HttpResponseRedirect(reverse('accounts:resetpass'))
def change_password(request,uidb64,token):
    try:
        link_check    = ResetPassword.objects.get(uidb64=uidb64, token=token)
        if link_check:
            form = ChangePasswordForm()
            user= Account.objects.get(id=urlsafe_base64_decode(uidb64))
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)
                if form.is_valid():
                    password    = request.POST['password']
                    user.set_password(password)
                    user.save()
                    link_check.delete()
                    messages.error(request, 'successfuly geandert')
                    return HttpResponseRedirect(reverse('accounts:login'))
                else:
                    return render(request,'shopapp/forgetpass.html',{'form':form})
                    form.errors()

            return render(request,'shopapp/forgetpass.html',{'form':form})
    except ResetPassword.DoesNotExist:
        raise Http404('not Foungd')

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
# Create your models here.
# Create a new Django app (optional)
# Create a custom User model.
# Substitute the default Django User model with yours.
# Create a custom Manager for the new User model.
# Register your new User model with Django admin (optional).
# Generate and run your migrations.
# Create your SuperUser.
#Add your new app to your INSTALLED_APPS Django setting, open your settings.py file and add:
#Extending the base class that Django has for User models.
#Removing the username field.
#Making the email field required and unique.
#Telling Django that you are going to use the email field as the USERNAME_FIELD.
#Removing the email field from the REQUIRED_FIELDS settings (it is automatically included as USERNAME_FIELD).
# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username/
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,username,last_name,email,password=None):
        if not email:
            raise ValueError('user must email adress haben')
        if not username:
            raise ValueError('User muss USERNAME haben')
        user=self.model(
            email      = self.normalize_email(email),
            username   = username,
            first_name = first_name,
            last_name  = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,email,first_name,last_name):
        user=self.create_user(
                email=self.normalize_email(email),
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
        )
        user.is_active     = True
        user.is_superadmin = True
        user.is_staff      = True
        user.is_active     = True
        user.is_admin     = True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    username        = models.CharField(max_length=22,unique=True)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(unique=True)
    phone_nummber   = models.CharField(max_length=15)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    #### diese Einstellung ist dafur, dass wie durch eamil authenticate konnen
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = ['username','first_name','last_name']
    # wir mussen dem Account model sagen,dass wir von MyAcountManager nutzen.
    objects=MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True

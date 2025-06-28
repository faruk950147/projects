from django.db import models
from django.http import HttpResponse
from based.models import BasedModels
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from django.utils.html import mark_safe

#account apps 
from account.managers import UserManager
from account.send_mail import send_account_activation_email
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator, ],
        unique=True
    )
    email = models.EmailField(
        max_length=150,
        unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", ]

    class Meta:
        ordering = ['-joined_date']
        verbose_name_plural = '1 User'

    def __str__(self):
        return f"{self.username}"

class Profile(BasedModels):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    username= models.CharField(max_length=150, null=True, blank=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    home_city = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    address1 = models.TextField(max_length=500, null=True, blank=True)
    address2 = models.TextField(max_length=500, null=True, blank=True)
    #account verify field
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=50, unique=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-joined_date']
        verbose_name_plural = '2 Profiles'
        
    @property
    def image_tag(self):   
        if self.profile_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.profile_image.url))
        else:
            self.profile_image
        
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            #email token generator
            email_token = str(uuid.uuid4())
            #create profile
            Profile.objects.create(user=instance, email_token=email_token)
            #verification email
            email = instance.email
            #send email
            send_account_activation_email(email_token, email)
        else:
            return HttpResponse('Profile has mot created')
    except Exception as e:
        print(e)
            
            

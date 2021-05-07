from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        user = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email, password, **kwargs):
        
        user = self.create_user(email, password, **kwargs)
        user.is_staff=True
        user.is_superuser=True
        user.save()

        return user




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return ''.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

    def  clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
from django.db import models
from django.contrib.auth.models import  PermissionsMixin, AbstractBaseUser
from v1.home.models import DefaultAbstract
from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, DefaultAbstract):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    # is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self, *args, **kwargs):
        return f"{self.first_name}, {self.phone}"

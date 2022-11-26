from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone



class CustomUser(AbstractUser):
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    biography = models.TextField(max_length=160, default="", blank=True, null=True)
    def __str__(self):
        return self.username

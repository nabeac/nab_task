from django.db import models
from django.contrib.auth.models import AbstractUser 


class User(AbstractUser):
    # phone = models.CharField(max_length=100, null=True, blank=True)
    # birth = models.DateField(null=True, blank=True)
    # admin = models.BooleanField(null=True,default=False)
    pass
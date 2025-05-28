import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    pass


def generic_code():
    return random.randint(100000,999000)


def exp_time_now():
    return timezone.now()+timedelta(minutes=2)


class Code(models.Model):
    code = models.PositiveIntegerField(default=generic_code)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='code')
    exp_date = models.DateTimeField(default=exp_time_now)
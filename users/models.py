from django.db import models
from django.contrib.auth.models import User

from polls.models import Choice


class MyUser(User):
    votes = models.ManyToManyField(Choice, 'users')

import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('publication date')

    def is_recent(self):
        """ Is the question published in last 24 hours? """
        now = timezone.now()
        return now - datetime.timedelta(days=3) <= self.pub_date <= now

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

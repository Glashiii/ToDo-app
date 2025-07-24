from django.contrib.auth.models import User
from django.db import models

from ToDo import settings


# Create your models here.

class Task(models.Model):
    task_text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='tasks' )
    task_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.task_text
from django.contrib.auth.models import User
from django.db import models


class TaskList(models.Model):
    manage = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.task + ' - ' + str(self.done)

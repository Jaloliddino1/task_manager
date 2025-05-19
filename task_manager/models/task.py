from django.db import models
from accounts.models import User
from task_manager.models.project import Project


class StatusChoice(models.TextChoices):
    TO_DO = 'to_do', 'To_Do'
    PROCESS = 'process', 'Process'
    TEST = 'test', 'Test'
    DONE = 'done', 'Done'


class Task(models.Model):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='task')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task_accounts')
    status = models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.TO_DO)

    class Meta:
        db_table = 'tasks'

from django.db import models
from accounts.models import User
from common.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='project_owner')
    members = models.ManyToManyField(User,related_name='project_members')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'

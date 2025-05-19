from rest_framework import serializers

from accounts.models import User
from task_manager.models import Project


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

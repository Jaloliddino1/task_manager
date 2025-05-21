from task_manager.views.project import (HelloAPIView,
                                        ProjectDetailAPIView,
                                        ProjectAPIView,
                                        ProjectViewSet)
from task_manager.views.task import TaskViewSet

__all__ = (
    HelloAPIView,
    ProjectAPIView,
    ProjectDetailAPIView,
    TaskViewSet,
)

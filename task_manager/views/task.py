from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from task_manager.models import Task
from task_manager.serializers import TaskListSerializers, TaskCreateAndUpdateSerializers, TaskDetailSerializers


# class TaskViewSet(ViewSet):
#
#     # get /task/
#     def list(self, request):
#         task = Task.objects.all()
#         serializers = TaskListSerializers(task, many=True)
#         return Response(serializers.data)
#
#     # get task/2/
#     def retrieve(self, request, pk, *args, **kwargs):
#         task = Task.objects.filter(id=pk).first()
#         serializers = TaskListSerializers(task)
#         return Response(serializers.data)
#
#     # put task/1/
#     def update(self, request, *args, **kwargs):
#         pass
#
#     def partial_update(self, request, pk, *args, **kwargs):
#         task = Task.objects.filter(id=pk).first()
#         serializers = TaskCreateAndUpdateSerializers(task, data=request.data, partial=True)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data)
#
#     # delete task/1/
#     def destroy(self, request, *args, **kwargs):
#         pass
#
#     # post task/
#     def create(self, request, *args, **kwargs):
#         serializers = TaskCreateAndUpdateSerializers(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data)

# class TaskViewSet(ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskCreateAndUpdateSerializers
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return TaskListSerializers
#         elif self.action == 'retrieve':
#             return TaskDetailSerializers
#         return self.serializer_class

class TaskViewSet(GenericViewSet,
                  ListModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializers

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializers
        return self.serializer_class


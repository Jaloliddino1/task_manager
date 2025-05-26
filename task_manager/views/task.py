from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from task_manager.models import Task
from task_manager.serializers import TaskListSerializers, TaskCreateAndUpdateSerializers, TaskDetailSerializers
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import filters


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
class CustomPagination(PageNumberPagination):
    page_size = 2  # Har bir sahifada 10 ta element
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateAndUpdateSerializers
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = ['title']
    filterset_fields = ['status', 'project']
    ordering_fields = ['created_at']

    # pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializers
        elif self.action == 'retrieve':
            return TaskDetailSerializers
        return self.serializer_class

    # def get_queryset(self):
    #     param = self.request.query_params.get('search')
    #     status = self.request.query_params.get('status')
    #     if param:
    #         # icontains search
    #         # return self.queryset.filter(title__icontains=param)
    #         # fuzzy search
    #         self.queryset = self.queryset.annotate(
    #             similarty=TrigramSimilarity('title', param)
    #         ).filter(similarty__gt=0.3).order_by('-similarty')
    #     if status:
    #         self.queryset = self.queryset.filter(status=status)
    #     return self.queryset

# class TaskViewSet(GenericViewSet,
#                   ListModelMixin,
#                   RetrieveModelMixin,
#                   DestroyModelMixin):
#     queryset = Task.objects.all()
#     serializer_class = TaskDetailSerializers
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return TaskListSerializers
#         return self.serializer_class

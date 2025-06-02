from django.db.models.functions import Trunc
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from task_manager.models import Project
from task_manager.serializers import ProjectListSerializer, ProjectDetailSerializers, ProjectCreateAndUpdateSerializers, \
    AddMemberSerializers


class HelloAPIView(APIView):
    def get(self, request):
        return Response({
            'message': 'Hello World'
        })


class ProjectAPIView(APIView):
    def get(self, request, pk=None):
        projects = Project.objects.all()
        serializers = ProjectListSerializer(projects, many=True)
        return Response(data=serializers.data)

    def post(self, request):
        serializer = ProjectCreateAndUpdateSerializers(data=request.data, context={'request': request})
        # if serializer.is_valid():
        #     data = serializer.validated_data
        #     Project.objects.create(
        #         name=data.get('name'),
        #         description=data.get('description'),
        #         owner=data.get('owner')
        #     )
        #     return Response({"message": "ok"}, status=201)
        # return Response(data=serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Project.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            owner=data.get('owner')
        )
        return Response({"message": "ok"}, status=201)


class ProjectDetailAPIView(APIView):
    def get(self, request, pk):
        project = Project.objects.filter(id=pk).first()
        serializer = ProjectDetailSerializers(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.filter(id=pk).first()
        serializer = ProjectCreateAndUpdateSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            project.name = data.get('name')
            project.description = data.get('description')
            project.owner = data.get('owner')
            project.save()
            return Response({"message": "ok"}, status=201)
        return Response(data=serializer.errors, status=400)


class ProjectViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    @action(methods=['post'], detail=True, serializer_class=AddMemberSerializers)
    def add_member(self, request, *args, **kwargs):
        project = self.get_object()
        serializers = AddMemberSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        project.members.add(serializers.validated_data.get('user'))
        return Response({"message": "ok"})

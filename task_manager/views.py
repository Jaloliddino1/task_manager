from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.models import Project
from task_manager.serializers import ProjectSerializer


class HelloAPIViev(APIView):
    def get(self,request):
        return Response({
            'message':'Hello World'
        })


class ProjectAPIView(APIView):
    def get(self,request):
        projects=Project.objects.all()
        serializers=ProjectSerializer(projects,many=True)
        return Response(data=serializers.data)





class ProjectDetailAPIViev(APIView):
    def get(self,request,pk):
       project=Project.objects.filter(id=pk).first()
       serialzers=ProjectSerializer(project)
       return Response(data=serialzers.data)
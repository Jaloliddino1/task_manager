import sys
from math import factorial

from celery.result import AsyncResult
from django.contrib.auth import login, logout
from U2_rest import celery_app
from accounts.tasks import add
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import UserRegisterSerializer, LoginSerializer, UserLightSerializer, TaskSerializer
from accounts.service import create_token

sys.set_int_max_str_digits(10000000)


class UserViewSet(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['session', 'logout', 'logout_token']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['login', 'login_with_token']:
            return LoginSerializer
        return self.serializer_class

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        return Response({"message": "ok"})

    # @action(methods=['post'], detail=False)
    # def login_with_token(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data.get('user')
    #     return (Response({"message": "ok", "token": user.token})

    @action(methods=['post'], detail=False)
    def login_with_token(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = create_token(user.id)
        return Response(token)

    @action(methods=['delete'], detail=False)
    def logout_token(self, request):
        request.user.auth_token.delete()
        return Response({"message": "ok"})

    @action(methods=['delete'], detail=False)
    def logout(self, request):
        logout(request)
        return Response({"message": "ok"})

    @action(methods=['get'], detail=False)
    def session(self, request):
        user = request.user
        serializers = UserLightSerializer(user)
        return Response(data=serializers.data)


class TestCeleryBackgroundView(GenericViewSet):

    @action(methods=['get'], detail=False)
    def test_celery(self, request):
        task = add.delay(15000000)
        return Response({"task_id": task.id})

    @action(methods=['post'], detail=False, serializer_class=TaskSerializer)
    def test_get_result(self, request):
        task_id = request.data.get('task_id')
        task = AsyncResult(str(task_id),app=celery_app)
        if task.ready():
            return Response({"result": str(task.result)})
        return Response({"result": "processing"})

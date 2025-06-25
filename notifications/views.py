from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.serializers import EmptySerializers
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_read=False)

    @action(methods=['get'], detail=False)
    def notification_count(self, request):
        return Response({"count": self.get_queryset().count()})

    @action(methods=['put'], detail=False, serializer_class=EmptySerializers)
    def all_marked_read(self, request):
        Notification.objects.all().update(is_read=True)
        return Response({"message": "ok"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.is_read = True
        instance.save()
        return Response(serializer.data)

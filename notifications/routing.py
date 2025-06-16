from django.urls import re_path

from notifications import consumers

websocket_urlpatterns=[
    re_path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]
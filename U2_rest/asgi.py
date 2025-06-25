import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import U2_rest.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'U2_rest.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": (
        URLRouter(
            U2_rest.routing.websocket_urlpatterns
        )
    ),
})
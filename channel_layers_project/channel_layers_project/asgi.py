import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "channel_layers_project.settings"
)

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()   # IMPORTANT

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import channel_layers_app.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            channel_layers_app.routing.websocket_urlpatterns
        )
    ),
})
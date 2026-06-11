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

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel_layers_project.settings')

# # ✅ Initialize Django BEFORE importing routing
# django_asgi_app = get_asgi_application()

# # Import routing AFTER Django is initialized
# from channel_layers_app.routing import websocket_urlpatterns

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(websocket_urlpatterns)
#     ),
# })

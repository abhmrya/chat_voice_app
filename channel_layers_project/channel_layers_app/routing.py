from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/sc', consumers.MySyncConsumer.as_asgi()),
    # path('ws/ac', consumers.MyAsyncConsumer.as_asgi()),
    # path('ws/index', consumers.IndexAsyncConsumer.as_asgi()),
    path('ws/online-status/', consumers.OnlineStatusConsumer.as_asgi()),
    path('ws/ac/<str:group_name>/', consumers.MyAsyncConsumer.as_asgi()),
    path('ws/oc/<str:user_name>/', consumers.OneToOneAsyncConsumer.as_asgi()),

]
# from django.urls import path
# from . import consumers

# websocket_urlpatterns = [
#     # path('ws/sc', consumers.MySyncConsumer.as_asgi()),
#     # path('ws/ac', consumers.MyAsyncConsumer.as_asgi()),
#     # path('ws/index', consumers.IndexAsyncConsumer.as_asgi()),
#     path('ws/online-status/', consumers.OnlineStatusConsumer.as_asgi()),
#     path('ws/ac/<str:group_name>/', consumers.MyAsyncConsumer.as_asgi()),
#     path('ws/oc/<str:user_name>/', consumers.OneToOneAsyncConsumer.as_asgi()),

# ]

from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/ac/(?P<group_name>\w+)/$", consumer.MyAsyncConsumer.as_asgi()),
    re_path(r"ws/oc/(?P<user_name>\w+)/$", consumer.OneToOneAsyncConsumer.as_asgi()),
    re_path(r"ws/online-status/$", consumer.OnlineStatusConsumer.as_asgi()),
]
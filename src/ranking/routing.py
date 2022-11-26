from django.urls import path
from . import consumers


websocket_urlpatterns = [
    # 元のコードは→url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    path('ws/rankpaged/<str:ranking_id>/', consumers.ChatConsumer.as_asgi()),
]

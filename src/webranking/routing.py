from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from ranking import routing
from django.core.asgi import get_asgi_application

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns,
#             #chat_routing.websocket_urlpatterns,
#         )
#     ),
# })
application = ProtocolTypeRouter( {
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack( URLRouter( routing.websocket_urlpatterns ) ),
} )

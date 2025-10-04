import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# Define o settings do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chat.settings")

# Inicializa o ASGI do Django
django_asgi_app = get_asgi_application()

# IMPORTA routing do app DEPOIS do setup
import ChatApp.routing

# Cria a aplicação ASGI com WebSocket
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns
        )
    ),
})

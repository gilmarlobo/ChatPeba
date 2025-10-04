import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack # Importação necessária para empacotar a rota
from channels.security.websocket import AllowedHostsOriginValidator # Importação CRÍTICA para Render
import ChatApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')

# 1. Configuração HTTP (usada para requisições Django normais, incluindo REST)
http_application = get_asgi_application()

# 2. Configuração WebSocket
websocket_application = AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns
        )
    )
)

# Roteador Principal
application = ProtocolTypeRouter({
    # Roteia requisições HTTP normais para o Django WSGI/ASGI
    "http": http_application, 
    
    # Roteia requisições WebSocket (ws:// ou wss://) para o Channel Layer
    # O AllowedHostsOriginValidator verifica se a origem (seu domínio) é confiável.
    "websocket": websocket_application,
})

"""
ASGI config for WebSocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from . import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSocket.settings')

# application = get_asgi_application()

# 支持websocket和http
application = ProtocolTypeRouter({
    "http" : get_asgi_application(), # 自动寻找urls.py  寻找视图函数 http
    "websocket" : URLRouter(routings.websocket_urlpatterns),  # routing(urls)   consumers(views)
})

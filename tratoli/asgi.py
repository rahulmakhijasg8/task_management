"""
ASGI config for tratoli project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.consumer import TaskUpdateConsumer


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/task_updates/', TaskUpdateConsumer.as_asgi()),
        ])
    ),
})


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tratoli.settings')

application = get_asgi_application()

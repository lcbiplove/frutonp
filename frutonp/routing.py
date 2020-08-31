from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from posts.consumers import CommentConsumer
from home.consumers import NotifConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('post/<int:post_id>/', CommentConsumer),
                    path('post/<int:post_id>/<int:comment_id>/', CommentConsumer),
                    path('post/<int:post_id>/<int:comment_id>/<int:reply_id>/', CommentConsumer),
                    path('home/', NotifConsumer),
                ]
            )
        )
    )
})
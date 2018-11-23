from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
from tasks.consumers import CommentUser
#
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # url(r"^messages/(?P<email>[\w.@+-]+)/$", ChatConsumer),
                    # url(r"^photo/(?P<id>\d+)/$", CommentConsumer),
                    # path('task-reviews/<int:pk>/', CommentUser),
                    path('task-detail/<slug:slug>/', CommentUser)
                    # re_path(r'^task-reviews/(?P<pk>\d+)/$', CommentUser)
                ]
            )
        )
    )
})

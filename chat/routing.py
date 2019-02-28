"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 18:32
-------------------------------------------------
"""
__author__ = 'lin'

from django.urls import path, re_path

from . import consumers

# websocket_urlpatterns = [ # 路由，指定 websocket 链接对应的 consumer
#     path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
# ]

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<group_name>[^/]+)/$', consumers.ChatConsumer),
    re_path(r'^push/(?P<username>[0-9a-z]+)/$', consumers.PushConsumer),
]
"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 18:25
-------------------------------------------------
"""
__author__ = 'lin'

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# 为Channels创建根路由配置 Channels 路由配置类似于Django URLconf
# 在与Channels开发服务器建立连接时，ProtocolTypeRouter将首先检查连接类型
# 如果它是WebSocket连接（ws：//或wss：//），则将连接到AuthMiddlewareStack。
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
    ),
})
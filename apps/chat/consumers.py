"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 18:33
-------------------------------------------------
"""
__author__ = 'lin'

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
# from medical.models import Messages
# from medical.serializers import MessagesSerializer

'''
class ChatConsumer(AsyncWebsocketConsumer):
    # ChatConsumer现在继承AsyncWebsocketConsumer而不是WebsocketConsumer。
    # 所有方法都是async def
    # await 用于调用执行I/O的异步函数。
    # async_to_sync 在通道层上调用方法时不再需要它。
    async def connect(self):
        # 'room_name' 为chat/routing.py的路由参数
        # 每个使用者都有一个范围，其中包含有关其连接的信息，
        # 特别是包括URL路由中的任何位置或关键字参数以及当前经过身份验证的用户（如果有）
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name应该是聊天室名字
        # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。
        # 组名只能包含字母，数字，连字符和句点。因此，此示例代码将在具有其他字符的房间名称上失败。
        self.room_group_name = 'chat_%s' % self.room_name

        # 加入小组 self.channel_layer.group_add
        # async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name) # 同步
        await self.channel_layer.group_add(self.room_group_name, self.channel_name) # 异步

        # 接受WebSocket连接
        # 如果不在connect()方法中调用accept()，则拒绝并关闭连接
        # 可能希望拒绝连接，因为请求的用户无权执行请求的操作
        # 如果选择接受连接，建议将accept()作为connect()中的最后一个操作调用
        await self.accept()

    async def disconnect(self, close_code):
        # 离开小组 self.channel_layer.group_discard
        # async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 将事件发送给组。
        # 事件具有'type'与应该在接收事件的使用者上调用的方法名称相对应的特殊键。
        # async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'chat_message', 'message': message})
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # self.send(text_data=json.dumps({'message': message}))
        await self.send(text_data=json.dumps({'message': message}))

'''

class ChatConsumer(AsyncJsonWebsocketConsumer):
    chats = dict()
    # ChatConsumer现在继承AsyncWebsocketConsumer而不是WebsocketConsumer。
    # 所有方法都是async def
    # await 用于调用执行I/O的异步函数。
    async def connect(self):
        # 每个使用者都有一个范围，其中包含有关其连接的信息，
        # 特别是包括URL路由中的任何位置或关键字参数以及当前经过身份验证的用户（如果有）
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # 将用户添加至聊天组信息chats中
        try:
            ChatConsumer.chats[self.group_name].add(self)
        except:
            ChatConsumer.chats[self.group_name] = set([self])

        #print(ChatConsumer.chats)
        # 创建连接时调用
        await self.accept()


    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 将该客户端移除聊天组连接信息
        ChatConsumer.chats[self.group_name].remove(self)
        await self.close()

    async def receive_json(self, message, **kwargs):
        # 收到信息时调用
        to_user = message.get('to_user')
        # 信息发送
        length = len(ChatConsumer.chats[self.group_name])
        if length == 2:
            await self.channel_layer.group_send(self.group_name,
                {"type": "chat.message", "message": message.get('message'), }, )
        else:
            await self.channel_layer.group_send(to_user,
                {"type": "push.message", "event": {'message': message.get('message'), 'group': self.group_name}}, )

    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        await self.send_json({"message": event["message"], })


# 推送consumer
class PushConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        # print(PushConsumer.chats)

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({"event": event['event']}))
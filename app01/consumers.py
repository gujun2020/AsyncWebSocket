from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端来向后端发送websocket连接的请求时，自动触发
        # 接受客户端的连接
        self.accept()

        # 获取群号，获取路由匹配中的
        self.group = self.scope['url_route']['kwargs'].get("group")

        # 将这个客户端的连接对象加入到存储结构中（ 内存 or redis ）
        async_to_sync(self.channel_layer.group_add)(self.group,self.channel_name) # 为当前客户端创建一个别名，加入群组"123"

        # 不接受连接
        # raise StopConsumer()
        # 给客户端主动发消息
        # self.send("我是服务端，正在给客户端发送消息")

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息
        text = message["text"]
        print("接受到的消息---->>>",text)
        if text == "关闭":
            # 服务端主动断开连接，并给客户端发送一条断开连接的消息
            self.close()
            return
        # 通知组内的所有客户端，执行chat_message方法，在此方法内自己定义任意的功能
        async_to_sync(self.channel_layer.group_send)(self.group,{"type":"chat_message","message":message})
        # self.close()
    def chat_message(self,event):
        text = event["message"]["text"]
        self.send(text)

    def websocket_disconnect(self, message):
        # 客户端和服务端断开连接时，自动触发
        async_to_sync(self.channel_layer.group_discard)(self.group,self.channel_name)
        raise StopConsumer()
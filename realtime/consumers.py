from channels.generic.websockets import JsonWebsocketConsumer
import socket
from realtime.models import Employee

class MyConsumer(JsonWebsocketConsumer):

    http_user = True
    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["realtime"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        """
        Called when a message is received with decoded JSON content
        """
        # Simple echo
        try:
            employee = Employee.objects.get(card_id = content['card_id'])
        except:
            status = 'denied'
        else:
            status = 'granted'
        try:
            self.socket_send(status)
        except:
            pass
        self.group_send('realtime',content)

    def socket_send(self,status):
        s = socket.socket()
        s.connect(("192.168.0.2", 1234))
        s.send("b'"+ status +"'")
        s.close()


    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass
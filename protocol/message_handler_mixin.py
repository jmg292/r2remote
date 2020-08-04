import base64

from .message import Message


class MessageHandlerMixin(object):

    def _write_line(self, message: bytes):
        self.socket.sendall(base64.b64encode(message) + b"\n")

    @staticmethod
    def _assemble_message_group(messages):
        messages.sort(key=lambda m: m.part)
        return ''.join([m.data for m in messages])

    def _get_message(self, message_wrapper, secure=True):
        message_group = []
        messages_remaining = 1
        while messages_remaining:
            # I want the JSON decoder to throw an error if it receives invalid data
            message_data = base64.b64decode(self.rfile.readline().strip())
            message = Message.unpack(message_data, message_wrapper, secure)
            messages_remaining = message.remaining_messages
            message_group.append(message)
        message = self._assemble_message_group(message_group)
        return message
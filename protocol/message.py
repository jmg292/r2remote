import json
import gzip

from typing import List


class Message(object):

    def __init__(self, data="", part=1, total=1, secure=True):
        self.part = part
        self.total = total
        self.data = data
        self._secure = secure

    @property
    def remaining_messages(self):
        return self.total - self.part

    def pack(self, message_wrapper):
        message_dict = {
            "part": self.part,
            "total": self.total,
            "data": self.data
        }
        message_data = gzip.compress(bytes(json.dumps(message_dict), 'utf-8'))
        return (message_wrapper.encrypt(message_data) if self._secure else message_data)

    @staticmethod
    def unpack(data, message_wrapper, secure=True):        
        message_dict = json.loads(
            gzip.decompress(
                message_wrapper.decrypt(data) if secure else data
            )
        )
        message_object = Message()
        for attribute in message_object.__dict__.keys():
            if not attribute.startswith("_"):
                setattr(message_object, attribute, message_dict[attribute])
        return message_object

    @staticmethod
    def from_string(message: str, max_size=32768, secure=True) -> List:
        message_chunks = [message[i:i+max_size] for i in range(0, len(message), max_size)]
        return [Message(message_chunks[i], i + 1, len(message_chunks), secure) for i in range(len(message_chunks))]

    @staticmethod
    def packed_from_string(message_wrapper, message: str, max_size=32768, secure=True) -> List:
        return [message.pack(message_wrapper) for message in Message.from_string(message, max_size, secure)]

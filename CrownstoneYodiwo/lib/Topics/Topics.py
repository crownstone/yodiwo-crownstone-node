from enum import Enum

class Topics(Enum):
    sendMessage = "sendMessage"  # data is a message
    receivedMessage = "receivedMessage"  # data is dict: { thingKey: str, payload: payload }
    
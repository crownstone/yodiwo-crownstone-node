from enum import Enum

class Topics(Enum):
    sendMessage = "sendMessage"  # data is single value: crownstoneId: int
    receivedMessage = "receivedMessage"  # data is dict: { thingKey: str, payload: payload }
    
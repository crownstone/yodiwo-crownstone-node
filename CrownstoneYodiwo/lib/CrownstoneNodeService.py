from CrownstoneYodiwo.lib.Topics.Topics import Topics

from CrownstoneYodiwo._EventBusInstance import CSEventBus
from Yodiwo import NodeService, Converter
from Yodiwo.lib import PyNodeHelper
from Yodiwo.lib.plegma.Messages import PortEventMsg, PortEvent



def getPortKey(key):
    arr = key.split("-")
    return arr[-1]


class CrownstoneNodeService(NodeService):
    indexedCrownstoneIds = []
    nodeService          = None
    
    def __init__(self, config):
        super().__init__(config)
        
    def registerThings(self, things):
        """
        Import things and post them to Yodiwo. This is a dict of Things, with key being the thingKey
        """
        self.ImportThings(things)
        

    def HandlePortEventMsg(self, msg):
        """
        This method handles incoming messages. These are events on input ports.
        """
        self._receiveMessage(msg)

    def start(self):
        CSEventBus.subscribe(Topics.sendMessage, self._sendMessage)
        self.Start(PyNodeHelper.eMessagingProtocol.Mqtt)

    def _receiveMessage(self, msg):
        for portevent in msg.PortEvents:
            selectedPort = None
            portevent = PortEvent.fromCloud(portevent)
            if portevent is not None:
                pk = portevent.PortKey
                thingKey = Converter.PortkeyToThingkey(pk)
                if thingKey in self._Things:
                    thing = self._Things[thingKey]
                    for p in thing.Ports:
                        if p.PortKey == pk:
                            p.State = portevent.State
                            selectedPort = getPortKey(pk)
                            break
    
                    CSEventBus.emit(Topics.receivedMessage, {"thingKey": thingKey, "port": selectedPort, "payload": portevent.State})
            else:
                print("Invalid PortEvent [missing attributes]. Ignoring...")
    

    def _sendMessage(self, msg):
        sequenceNumber = 1
        retries = 2
    
        message = PortEventMsg(sequenceNumber, msg)
        self.mqttclient.SendMsg(message, retries)  # send data to external
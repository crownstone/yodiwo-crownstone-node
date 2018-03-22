from Yodiwo import NodeService, Converter
from Yodiwo.lib import PyNodeHelper
from Yodiwo.lib.plegma.Messages import PortEventMsg, PortEvent

from CrownstoneYodiwo.lib.SharedVariables import THING_ID_BASE_NAME


def getPortKey(key):
    arr = key.split("-")
    return arr[-1]


class CrownstoneNodeService(NodeService):
    indexedCrownstoneIds = []
    nodeService          = None
    
    def __init__(self, config):
        super().__init__(config)
        
    def registerCrownstones(self, things):
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
        self.Start(PyNodeHelper.eMessagingProtocol.Mqtt)

    def _receiveMessage(self, msg):
        for portevent in msg.PortEvents:
            selectedPort = None
            
            portevent = PortEvent(**portevent)
            pk = portevent.PortKey
            thingKey = Converter.PortkeyToThingkey(pk)
            thing = self._Things[thingKey]
            for p in thing.Ports:
                if p.PortKey == pk:
                    p.State = portevent.State
                    selectedPort = getPortKey(pk)
                    break
        
            thingKeyExpanded = thingKey.split(THING_ID_BASE_NAME)
        
            # if there is not a single result, we can't parse this key
            if len(thingKeyExpanded) != 1:
                print("Invalid key:", thingKey, thingKeyExpanded)
                continue
        
            # use the selectedPort to trigger an action
            if thingKeyExpanded[0] == "SphereController":
                # get the crownstone we want to control based on the message stoneId
                pass
            else:
                pass

    def _sendMessage(self, msg):
        sequenceNumber = 1
        retries = 2
    
        message = PortEventMsg(sequenceNumber, msg)
        self.mqttclient.SendMsg(message, retries)  # send data to external
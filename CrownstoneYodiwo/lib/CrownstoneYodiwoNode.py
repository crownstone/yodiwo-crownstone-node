from Yodiwo import NodeService, Converter
from Yodiwo.lib.plegma.Messages import PortEventMsg, PortEvent

from BluenetLib import Bluenet

from CrownstoneYodiwo.lib.Crownstone import Crownstone

THING_ID_BASE_NAME = "crownstoneThing-"

def getPortKey(key):
    arr = key.split("-")
    return arr[-1]


class CrownstoneYodiwoNode(NodeService):
    indexedCrownstoneIds = []
    masterThing = None
    bluenet = None
    
    def __init__(self, bluenet):
        super().__init__()
        self.bluenet = bluenet
        
        self.initAvailableStones()
        self.enableDynamicCreation()
        

    def initAvailableStones(self):
        availableCrownstoneIds = Bluenet.getAvailableStoneIds()
        thingsDict = self.createThingsDict(availableCrownstoneIds)
        self.registerCrownstones(thingsDict)

    def enableDynamicCreation(self):
        # subscribe to new crownstone found ids.
        eventBus = self.bluenet.getEventBus()
        topics = self.bluenet.getTopics()
        eventBus.subscribe(topics.newCrownstoneFound, self.handleNewCrownstone)
        
        
    def createThingsDict(self, crownstoneIds):
        thingsDict = {}
        for stoneId in crownstoneIds:
            if stoneId not in self.indexedCrownstoneIds:
                stone = Crownstone(stoneId, self.bluenet, lambda msg: self._sendMessage(msg))
                thingsDict[(THING_ID_BASE_NAME + str(stoneId))] = stone.getThing()
                self.indexedCrownstoneIds.append(stoneId)
    
        return thingsDict
        
        
    def handleNewCrownstone(self,stoneId):
        thingsDict = self.createThingsDict([stoneId])
        self.registerCrownstones(thingsDict)
        
        
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
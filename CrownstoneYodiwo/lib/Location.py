import json

from BluenetLib import Bluenet, BluenetEventBus
from CrownstoneYodiwo._EventBusInstance import CSEventBus

from CrownstoneYodiwo.lib.Topics.Topics import Topics
from Yodiwo import Port, ConfigParameter, Thing, ThingUIHints
from Yodiwo.Enums import PortConfig, PortTypes, IODirection
from Yodiwo.lib.plegma.Messages import PortEvent
from BluenetLib import Topics as BluenetTopics

from CrownstoneYodiwo.lib.ports.InputPorts     import InputPorts
from CrownstoneYodiwo.lib.ports.OutputPorts    import OutputPorts

class Location:
    locationId    = None
    locationData  = None
    bluenet       = None
    
    def __init__(self, thingKey, locationData, bluenet):
        self.locationId   = locationData['id']
        self.locationData = locationData
        self.bluenet      = bluenet
        self.thingKey     = thingKey
        
        self.setupEventStream()
        

    def setupEventStream(self):
        BluenetEventBus.subscribe(BluenetTopics.personEnteredLocation, self._handlePersonEnter)
        BluenetEventBus.subscribe(BluenetTopics.personLeftLocation, self._handlePersonExit)
    
    def _handlePersonEnter(self, data):
        if str(data["locationId"]) == str(self.locationId):
            msg = [PortEvent(self.thingKey + "-" + OutputPorts.personEnter, json.dumps(data), None)]
            CSEventBus.emit(Topics.sendMessage, msg)
    
    def _handlePersonExit(self, data):
        if str(data["locationId"]) == str(self.locationId):
            msg = [PortEvent(self.thingKey + "-" + OutputPorts.personExit, json.dumps(data), None)]
            CSEventBus.emit(Topics.sendMessage, msg)
    
    def handleCommand(self, command, payload):
        pass

    def getThing(self):
        ports = []
        ports += self._generateInputPorts()
        ports += self._generateOutputPorts()
        ports += self._generateCombinedPorts()
        
        print("ROOM KEY", self.thingKey)
        return Thing(
            self.thingKey,
            self.locationData["name"] + " (#" + str(self.locationId) + ")",
            [ConfigParameter("Location Thing", "test")],
            ports,
            "com.yodiwo.text.default",
            None,
            False,
            ThingUIHints(
                IconURI="https://crownstone.rocks/images/icons/crownstone.png",
                Description=""
            )
        )
    
    
    def _generateInputPorts(self):
        inputPortList = []
        # inputPortList.append(
        #     Port(
        #         self.thingKey + "-" + InputPorts.switch.value,    # portkey
        #         "Switch Crownstone", # name
        #         "Provide a value [0 or 1] to switch the Crownstone off or on", # description
        #         IODirection.Input,  # io direction
        #         PortTypes.Decimal,  # type
        #         0,                  # initial state
        #         0,                  # revNum            (?)
        #         3                   # ePortConf enum    (?)
        #     )
        # )
        #
        return inputPortList

    def _generateCombinedPorts(self):
        combinedPortList = []
        # combinedPortList.append(
        #     Port(
        #         self.thingKey + "-" + InputPorts.switch.value,  # portkey
        #         "Switch Crownstone",  # name
        #         "Provide a value [0 or 1] to switch the Crownstone off or on",  # description
        #         IODirection.Input,  # io direction
        #         PortTypes.Decimal,  # type
        #         0,  # state     (?)
        #         0,  # revNum    (?)
        #         3  # confFlags (?)
        #     )
        # )
    
        return combinedPortList
        

    def _generateOutputPorts(self):
        outputPortList = []
        outputPortList.append(
            Port(
                self.thingKey + "-" + OutputPorts.personEnter.value,  # portkey
                "Person enter event",  # name
                "User data of a user who enters this location",  # description
                IODirection.Output,  # io direction
                PortTypes.JsonString,   # data type
                "{}",                   # initial state
                0,                   # revNum            (?)
                3                    # ePortConf enum    (?)
            )
        )
        outputPortList.append(
            Port(
                self.thingKey + "-" + OutputPorts.personExit.value,  # portkey
                "Person exit event",  # name
                "User data of a user who leaves this location",  # description
                IODirection.Output,  # io direction
                PortTypes.JsonString,  # data type
                "{}",  # initial state
                0,  # revNum            (?)
                3  # ePortConf enum    (?)
            )
        )
        
        return outputPortList

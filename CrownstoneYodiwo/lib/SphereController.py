import json

from CrownstoneYodiwo.lib.Topics.Topics import Topics
from CrownstoneYodiwo._EventBusInstance import CSEventBus

from Yodiwo.Enums import PortConfig, PortTypes, IODirection
from CrownstoneYodiwo.lib.ports.InputPorts import InputPorts
from Yodiwo import ThingUIHints, ConfigParameter, Port, Thing


class SphereController:
    thingKey = None
    sphereData = None
    sphereId = None
    bluenet = None
    
    def __init__(self, thingKey, sphereData, bluenet):
        self.thingKey = thingKey
        self.sphereId = sphereData["cloudId"]
        self.sphereData = sphereData
        self.bluenet = bluenet
        
        self.setupEventStream()

    def setupEventStream(self):
        CSEventBus.subscribe(Topics.receivedMessage, self.handleCommand)


    def handleCommand(self, data):
        thingKey = data["thingKey"]
        port = data["port"]
        payloadStr = data["payload"]
        

        # event is NOT for this controller
        if self.thingKey != thingKey:
            return
    
        payload = json.loads(payloadStr)
        
        if port == InputPorts.switch.value:
            self.bluenet.switchCrownstone(payload["id"], float(payload["switchState"]) == 1)



    def getThing(self):
        ports = []
        ports += self._generateInputPorts()
        ports += self._generateOutputPorts()
        ports += self._generateCombinedPorts()
    
        return Thing(
            self.thingKey,
            self.sphereData["name"],
            [ConfigParameter("Crownstone Sphere Controller", "Lorem Ipsum")],
            ports,
            "com.crownstone.sphere",
            None,
            False,
            ThingUIHints(
                IconURI="https://crownstone.rocks/images/icons/ai.png",
                Description=""
            )
        )

    def _generateInputPorts(self):
        inputPortList = []
        inputPortList.append(
            Port(
                self.thingKey + "-" + InputPorts.switch.value,  # portkey
                "Switch Crownstone by ID",  # name
                "Provide a json {id: crownstondId, switchState: [0 or 1]}",  # description
                IODirection.Input,  # io direction
                PortTypes.JsonString,  # type
                0,  # initial state
                0,  # revNum            (?)
                0  # ePortConf enum    (?)
            )
        )
    
        return inputPortList

    def _generateCombinedPorts(self):
        combinedPortList = []
        # combinedPortList.append(
        #     Port(
        #         self.thingKey + "-" + CombinedPorts.isAvailable.value,  # portkey
        #         "Available",  # name
        #         "Check if a Crownstone is Available to use via the Mesh",  # description
        #         IODirection.InputOutput,  # io direction
        #         PortTypes.Boolean,  # type
        #         False,  # state     (?)
        #         0,  # revNum    (?)
        #         0   # confFlags (?)
        #     )
        # )
    
        return combinedPortList

    def _generateOutputPorts(self):
        outputPortList = []
        # outputPortList.append(
        #     Port(
        #         self.thingKey + "-" + OutputPorts.powerUsage.value,  # portkey
        #         "Power measurement in W",  # name
        #         "Event of power measurements of this Crownstone",  # description
        #         IODirection.Output,  # io direction
        #         PortTypes.Decimal,  # data type
        #         0,  # initial state
        #         0,  # revNum            (?)
        #         0   # ePortConf enum    (?)
        #     )
        # )
    
        return outputPortList

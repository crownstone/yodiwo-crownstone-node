from BluenetLib import Bluenet, BluenetEventBus
from CrownstoneYodiwo.lib.ports.CombinedPorts import CombinedPorts

from CrownstoneYodiwo._EventBusInstance import CSEventBus

from CrownstoneYodiwo.lib.Topics.Topics import Topics
from Yodiwo import Port, ConfigParameter, Thing, ThingUIHints
from Yodiwo.Enums import PortConfig, PortTypes, IODirection
from Yodiwo.lib.plegma.Messages import PortEvent
from BluenetLib import Topics as BluenetTopics

from CrownstoneYodiwo.lib.ports.InputPorts     import InputPorts
from CrownstoneYodiwo.lib.ports.OutputPorts    import OutputPorts

class Crownstone:
    stoneId    = None
    stoneData  = None
    bluenet    = None
    thingKey   = None
    
    def __init__(self, thingKey, stoneData, bluenet):
        self.stoneId   = stoneData['id']
        self.stoneData = stoneData
        self.bluenet   = bluenet
        self.thingKey  = thingKey
        
        self.setupEventStream()
        

    def setupEventStream(self):
        CSEventBus.subscribe(Topics.receivedMessage, self.handleCommand)
        BluenetEventBus.subscribe(BluenetTopics.powerUsageUpdate,    self._updatePowerMeasurement)
        BluenetEventBus.subscribe(BluenetTopics.crownstoneAvailable, self._updateAvailable)

    def _updatePowerMeasurement(self, bluenetData):
        """
        :param bluenetData: data dict from bluenet {'crownstoneId': number, 'powerUsage': float}
        :return:
        """
        if str(bluenetData['id']) == str(self.stoneId):
            msg = [PortEvent(self.thingKey + "-" + OutputPorts.powerUsage.value, str(max(0.0,float(bluenetData["powerUsage"]))), None)]
            CSEventBus.emit(Topics.sendMessage, msg)
            
    def _updateAvailable(self, data):
        if str(data['id']) == str(self.stoneId):
            self.stoneData = data
            msg = [PortEvent(self.thingKey + "-" + CombinedPorts.isAvailable.value, self.stoneData["available"], None)]
            CSEventBus.emit(Topics.sendMessage, msg)

    def handleCommand(self, data):
        thingKey = data["thingKey"]
        port = data["port"]
        payload = data["payload"]

        if self.thingKey == thingKey:
            if port == InputPorts.switch.value:
                self.bluenet.switchCrownstone(self.stoneId, float(payload) == 1)
            elif port == CombinedPorts.isAvailable.value:
                if bool(payload):
                    self._updateAvailable(self.stoneData)

    def getThing(self):
        ports = []
        ports += self._generateInputPorts()
        ports += self._generateOutputPorts()
        ports += self._generateCombinedPorts()
        
        return Thing(
            self.thingKey,
            self.stoneData["name"] + " (#" + str(self.stoneId) + ")",
            [ConfigParameter("Crownstone Thing", "test")],
            ports,
            "com.crownstone.crownstone",
            None,
            False,
            ThingUIHints(
                IconURI="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/e3/1f/57/e31f57d8-4c30-b6fd-fb42-9b160f2b2db0/AppIcon-1x_U007emarketing-85-220-0-4.png/230x0w.jpg",
                Description=""
            )
        )
    
    
    def _generateInputPorts(self):
        inputPortList = []
        inputPortList.append(
            Port(
                self.thingKey + "-" + InputPorts.switch.value,    # portkey
                "Switch Crownstone", # name
                "Provide a value [0 or 1] to switch the Crownstone off or on", # description
                IODirection.Input,  # io direction
                PortTypes.Decimal,  # type
                0,                  # initial state
                0,                  # revNum            (?)
                0                   # ePortConf enum    (?)
            )
        )
        
        return inputPortList

    def _generateCombinedPorts(self):
        combinedPortList = []
        combinedPortList.append(
            Port(
                self.thingKey + "-" + CombinedPorts.isAvailable.value,  # portkey
                "Available",  # name
                "Check if a Crownstone is Available to use via the Mesh",  # description
                IODirection.InputOutput,  # io direction
                PortTypes.Boolean,  # type
                False,  # state     (?)
                0,      # revNum    (?)
                3       # confFlags (?)
            )
        )
    
        return combinedPortList
        

    def _generateOutputPorts(self):
        outputPortList = []
        outputPortList.append(
            Port(
                self.thingKey + "-" + OutputPorts.powerUsage.value,  # portkey
                "Power measurement in W",  # name
                "Event of power measurements of this Crownstone",  # description
                IODirection.Output,  # io direction
                PortTypes.Decimal,   # data type
                0,                   # initial state
                0,                   # revNum            (?)
                0                    # ePortConf enum    (?)
            )
        )
        
        return outputPortList

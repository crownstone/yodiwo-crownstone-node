from BluenetLib import Bluenet
from Yodiwo import Port, ConfigParameter, Thing, ThingUIHints
from Yodiwo.Enums import PortConfig, PortTypes, IODirection
from Yodiwo.lib.plegma.Messages import PortEvent

from CrownstoneYodiwo.lib.SharedVariables      import THING_ID_BASE_NAME
from CrownstoneYodiwo.lib.ports.InputPorts     import InputPorts
from CrownstoneYodiwo.lib.ports.OutputPorts    import OutputPorts

class Crownstone:
    stoneId    = None
    stoneData  = None
    bluenet    = None
    sendMethod = None
    
    def __init__(self, stoneData, bluenet):
        self.stoneId   = stoneData['id']
        self.stoneData = stoneData
        self.bluenet   = bluenet
        self.thingKey  = THING_ID_BASE_NAME + str(self.stoneId )
        

    def setupEventStream(self):
        bluenetEventBus = self.bluenet.getEventBus()
        bluenetTopics   = self.bluenet.getTopics()
    
        bluenetEventBus.subscribe(bluenetTopics.powerUsageUpdate, self._updatePowerMeasurement)

    def _updatePowerMeasurement(self, data):
        msg = [PortEvent(self.thingKey + "-" + OutputPorts.powerUsage, str(data["powerUsage"]), None)]
        # self.sendMethod(msg)

    def handleCommand(self, command, payload):
        if command == InputPorts.switch:
            # todo parse payload
            Bluenet.switchCrownstone(self.stoneId, payload)

    def getThing(self):
        ports = []
        ports += self._generateInputPorts()
        ports += self._generateOutputPorts()
        
        return Thing(
            self.thingKey,
            "Crownstone " + str(self.stoneId),
            [ConfigParameter("Crownstone Thing", "test")],
            ports,
            "com.yodiwo.text.default",
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
                0,                  # state     (?)
                0,                  # revNum    (?)
                3                   # confFlags (?)
            )
        )
        
        return inputPortList
        

    def _generateOutputPorts(self):
        outputPortList = []
        outputPortList.append(
            Port(
                self.thingKey + "-" + OutputPorts.powerUsage.value,  # portkey
                "Power measurement in W",  # name
                "Event of power measurements of this Crownstone",  # description
                IODirection.Output,  # io direction
                PortTypes.Decimal,   # type
                0,                   # state     (?)
                0,                   # revNum    (?)
                3                    # confFlags (?)
            )
        )
        
        return outputPortList

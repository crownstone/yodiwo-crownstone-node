from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.util.JsonFileStore import JsonFileStore
from Yodiwo.lib import PyNodeHelper

from BluenetLib import Bluenet
from BluenetLib import Topics as BluenetTopics

from CrownstoneYodiwo.lib.Crownstone import Crownstone
from CrownstoneYodiwo.lib.CrownstoneNodeService import CrownstoneNodeService
from CrownstoneYodiwo.lib.SharedVariables import THING_ID_BASE_NAME


def getPortKey(key):
    arr = key.split("-")
    return arr[-1]


class CrownstoneYodiwoNode:
    indexedCrownstoneIds = []
    masterThing          = None
    bluenet              = None
    bluenetCloud         = None
    bluenetCloudSphere   = None
    
    nodeService          = None
    
    def __init__(self):
        self.bluenet = Bluenet(catchSIGINT=False)
        self.bluenetCloud = self.bluenet.getCloud()
        
        
    def loadConfig(self, path):
        fileReader = JsonFileStore(path)
        data = fileReader.getData()
        
        csUser = data["crownstoneUser"]
        
        self.bluenetCloud.setUserInformation(
            email=csUser["email"],
            password=csUser["password"],
            sha1Password=csUser["sha1Password"],
            accessToken=csUser["accessToken"]
        )
        
        if "sphereId" in csUser and csUser["sphereId"] != "":
            self.bluenetCloudSphere = self.bluenetCloud.getSphereHandler(csUser["sphereId"])
        elif "sphereName" in csUser and csUser["sphereName"] != "":
            self.bluenetCloudSphere = self.bluenetCloud.getSphereHandlerByName(csUser["sphereName"])

        if self.bluenetCloudSphere is None:
            raise Exception("Sphere not found in cloud, check the id or name.")
        
        # download stones for bluenet
        self.bluenetCloudSphere.getStones()
        
        # init Crownstone USB
        self.bluenet.initializeUSB(data["bluenet"]["usbPort"])
        
        # init Yodiwo Service
        yodiwoData = data["yodiwoUser"]
        yodiwoConfig = PyNodeHelper.ConfigContainer()
        yodiwoConfig.setData(yodiwoData)
        self.nodeService = CrownstoneNodeService(yodiwoConfig)
        
        
    def start(self):
        self.initAvailableStones()
        self.enableDynamicCreation()
        self.nodeService.start()
        

    def initAvailableStones(self):
        availableCrownstonesDict = self.bluenet.getCrownstones()
        arrayOfStoneDicts = []
        for stoneId, stoneData in availableCrownstonesDict.items():
            arrayOfStoneDicts.append(stoneData)
        
        thingsDict = self.createThingsDict(arrayOfStoneDicts)
        self.nodeService.registerCrownstones(thingsDict)

    def enableDynamicCreation(self):
        # subscribe to new crownstone found ids.
        BluenetEventBus.subscribe(BluenetTopics.crownstoneAvailable, self.handleNewCrownstone)
        
        
    def createThingsDict(self, crownstoneDictionary):
        thingsDict = {}
        for stone in crownstoneDictionary:
            if stone['id'] not in self.indexedCrownstoneIds:
                cs = Crownstone(stone, self.bluenet)
                key = THING_ID_BASE_NAME + str(stone['id'])
                thingsDict[key] = cs.getThing()
                self.indexedCrownstoneIds.append(stone['id'])
    
        return thingsDict
        
        
    def handleNewCrownstone(self,stoneId):
        thingsDict = self.createThingsDict([stoneId])
        self.nodeService.registerCrownstones(thingsDict)
        
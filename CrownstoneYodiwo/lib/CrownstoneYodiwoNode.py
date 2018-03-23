from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.util.JsonFileStore import JsonFileStore
from Yodiwo.lib import PyNodeHelper

from BluenetLib import Bluenet
from BluenetLib import Topics as BluenetTopics

from CrownstoneYodiwo.lib.Crownstone import Crownstone
from CrownstoneYodiwo.lib.CrownstoneNodeService import CrownstoneNodeService
from CrownstoneYodiwo.lib.Location import Location


def getPortKey(key):
    arr = key.split("-")
    return arr[-1]


class CrownstoneYodiwoNode:
    indexedCrownstoneIds = []
    indexedLocationIds   = []
    masterThing          = None
    bluenet              = None
    bluenetCloud         = None
    bluenetCloudSphere   = None
    
    nodeService          = None
    config               = None
    yodiwoConfig         = None
    sphereData           = None
    
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
        
        self.sphereData = self.bluenetCloudSphere.getSphereData()
        
        # init Crownstone USB
        self.bluenet.initializeUSB(data["bluenet"]["usbPort"])
        
        # init Yodiwo Service
        yodiwoData = data["yodiwoUser"]
        yodiwoConfig = PyNodeHelper.ConfigContainer()
        yodiwoConfig.setData(yodiwoData)
        self.yodiwoConfig = yodiwoConfig
        self.nodeService = CrownstoneNodeService(yodiwoConfig)
        
        
    def start(self):
        self.initLocations()
        self.initAvailableStones()
        self.enableDynamicCreation()
        self.nodeService.start()
        

    def initLocations(self):
        avaliableLocations = self.bluenetCloudSphere.getLocations()
        thingsDict = {}
        for location in avaliableLocations:
            if location['id'] not in self.indexedLocationIds:
                thingKey = self.yodiwoConfig.nodekey.toString() + '-L' + str(location['id'])
                loc = Location(thingKey, location, self.bluenet)
                thingsDict[thingKey] = loc.getThing()
                self.indexedLocationIds.append(location['id'])

        self.nodeService.registerThings(thingsDict)
        

    def initAvailableStones(self):
        availableCrownstonesDict = self.bluenet.getCrownstones()
        arrayOfStoneDicts = []
        for stoneId, stoneData in availableCrownstonesDict.items():
            arrayOfStoneDicts.append(stoneData)
        
        thingsDict = self.createThingsDict(arrayOfStoneDicts)
        
        self.nodeService.registerThings(thingsDict)
        
    def initSphereController(self):
        pass
    
    def initDataStore(self):
        pass

    def enableDynamicCreation(self):
        # subscribe to new crownstone found ids.
        BluenetEventBus.subscribe(BluenetTopics.crownstoneAvailable, self.handleNewCrownstone)
        
        
    def createThingsDict(self, crownstoneArray):
        thingsDict = {}
        for stone in crownstoneArray:
            if stone['id'] not in self.indexedCrownstoneIds:
                thingKey = self.yodiwoConfig.nodekey.toString() + '-CS' + str(stone['id'])
                cs = Crownstone(thingKey, stone, self.bluenet)
                thingsDict[thingKey] = cs.getThing()
                self.indexedCrownstoneIds.append(stone['id'])
    
        return thingsDict
        
        
    def handleNewCrownstone(self,stoneId):
        thingsDict = self.createThingsDict([stoneId])
        self.nodeService.registerThings(thingsDict)
        
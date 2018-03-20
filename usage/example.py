from CrownstoneYodiwo.lib.CrownstoneSphereController import CSMasterThing

from BluenetLib import Bluenet

from CrownstoneYodiwo.lib.CrownstoneYodiwoNode import CrownstoneYodiwoNode

bluenet = Bluenet()
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART", catchSIGINT=True)

service = CrownstoneYodiwoNode(bluenet)














# create master Thing for this sphere ( sphere is unknown, based on discovery )

# load user config ( node ID, node Secret, yodiwo server details, rest endpoint )

# load initially discovered stones to Things

# subscribe to automatically update the Things based on the discovery

## cloud links ?

# load user config ( crownstone username / password / accessToken )

# subscribe webhooks on events from localization

# yodiwo-crownstone-node

Crownstone python node for the Yodiwo platform. 

To use this node, we expect the Crownstone USB dongle is connected to the device running this node.

This node is written in Python 3 and requires Python 3.5 or higher. For the installation process `setuptools` is required.

```
sudo apt install python3 python3-setuptools
```

To install the module run:

### Installation

```
python3 setup.py install
```

You will then need to create a nodeConfig.json file. There is a template provided in the ./usage folder.

### Config

Lets try to create a config file! You can copy paste the template file in the ./usage folder and rename it to nodeConfig.json. Open it in a text editor.

```
{
  "crownstoneUser":{
    "email":"",
    "password":"",
    "sha1Password":"",
    "accessToken":"",
    "sphereId":"",
    "sphereName":""
  },
  "yodiwoUser":{
    "ActiveID": "dev4cyan",
    "Configs": {
      "dev4cyan": {
        "NodeKey": " ",
        "NodeName": "PyNode",
        "NodeSecret": "",
        "MqttBrokerCertFile": null,
        "MqttBrokerHostname": "dev4cyan.yodiwo.com",
        "MqttUseSsl": true
      }
    }
  },
  "bluenet":{
    "usbPort":"/dev/tty.SLAB_USBtoUART"
  }
}
```

We start with the crownstoneUser field.

```
"crownstoneUser":{
    "email":"",
    "password":"",
    "sha1Password":"",
    "accessToken":"",
    "sphereId":"",
    "sphereName":""
}
```

There are a few required fields in this config. For the user part (email, password, sha1Password, accessToken) You can either:
- supply an accessToken
- supply an email address and password (that are used for the Crownstone service [https://my.crownstone.rocks])
- supply an email address and a sha1 hash of your password (like abcde is hashed to 03de6c570bfe24bfc328ccd7ca46b76eadaf4334)

For the sphere part (sphereId, sphereName) you can either specify an SphereId (which you can look up in the Crownstone Cloud) or just the name of your Sphere in the Crownstone app.

The Bluenet part:

```
"bluenet":{
    "usbPort":"/dev/tty.SLAB_USBtoUART"
}
```

Specifies on which port the user can find the Crownstone USB dongle. For more information on this, take a look at the bluenet lib [https://github.com/crownstone/bluenet-python-lib].

Finally, the Yodiwo part:

```
"yodiwoUser":{
    "ActiveID": "dev4cyan",
    "Configs": {
        "dev4cyan": {
        "NodeKey": " ",
        "NodeName": "PyNode",
        "NodeSecret": "",
        "MqttBrokerCertFile": null,
        "MqttBrokerHostname": "dev4cyan.yodiwo.com",
        "MqttUseSsl": true
        }
    }
}
```

This is explained over at the Yodiwo python agent: [https://github.com/crownstone/yodiwo-python-node].

### Running the node.

When you have completed the installation and you have your config json, you can run the node. In the ./usage folder we have an example of how this is done.

```python

from CrownstoneYodiwo import CrownstoneNode

node = CrownstoneNode()
node.loadConfig('nodeConfig.json') # the path tho this config is relative to file containing this line of code
node.start()

```

Have fun!

# Execution / Deployment

There are only a few steps:

    cd conf
    cp yodiwo-crownstone.conf.default yodiwo-crownstone.conf
    # edit yodiwo-crownstone.conf with access details
    cd scripts
    sudo ./install

You can test with `./run`.

## Control syslog file size

In your deployment setup you likely want to limit the log files, so they can't suddenly spin out of control if a process decides to spit out a huge amount of information:

    sudo mkdir -p /etc/systemd/journald.conf.d
    sudo vim /etc/systemd/journald.conf.d/size.conf

Make sure the file has the following content:

    [Journal]
    SystemMaxUse=250M
    SystemMaxFileSize=50M

If there is too much information shown on Debug levels you can limit the logs to the Warning level:

    sudo vim /etc/systemd/journald.conf.d/level.conf

And contents:

    [Journal]
    # not save all levels but only 0 to 4
    MaxLevelStore=warning

# Copyright

For information about licensing and copyright, contact Crownstone (https://crownstone.rocks).




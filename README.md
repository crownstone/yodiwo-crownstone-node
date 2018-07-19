# yodiwo-crownstone-node

Crownstone Python node for the [Yodiwo platform](https://www.yodiwo.com/).

To use this node, we expect the [Crownstone USB dongle](https://shop.crownstone.rocks/products/crownstone-usb-dongle) is connected to the device running the Crownstone Python node.

## Hardware preparation

On the Cyient gateway, you will need the proper kernel drivers, update the module dependencies, and modprobe the module.

    sudo cp usbserial.ko /lib/modules/$(uname -r)/kernel/drivers/usb/serial
    sudo cp cp201x.ko /lib/modules/$(uname -r)/kernel/drivers/usb/serial
    sudo depmod -a
    sudo modprobe cp201x

This should not lead to errors. If this works, edit `/etc/modules` and add `cp201x` on one of the lines.

If you now plug-in the Crownstone USB dongle, you should see a device node in the `/dev` directory, for example `/dev/ttyUSB0`.

## Software Prerequisites 

This node is written in Python 3 and requires Python 3.5 or higher. For the installation process `setuptools` is required.

```
sudo apt install python3 python3-setuptools
```

You will then need a configuration file. There is a template provided in the `./conf` folder.

## Software Configuration

Copy template and open it a text editor:

```
cd conf
cp yodiwo-crownstone.conf.default yodiwo-crownstone.conf
```

### Crownstone network configuration

Adjust the crownstoneUser field in `yodiwo-crownstone.conf`.

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

There are a few required fields in this config for the `crownstoneUser`. 

1. You can either (only one of these required) specify:
- an `accessToken`;
- an `email` address and `password` (the ones which are used for the [Crownstone service](https://my.crownstone.rocks));
- an `email` address and a `sha1` hash of your password (for example `abcde` is hashed to `03de6c570bfe24bfc328ccd7ca46b76eadaf4334`).

2. For the sphere part (`sphereId`, `sphereName`) you have to specify (only one of these are required):
- a `SphereId` (which you can look up in the Crownstone Cloud);
- or just the `name` of your Sphere (which you can look up in the Crownstone app).

### Crownstone hardware configuration

The Bluenet part:

```
"bluenet":{
    "usbPort":"/dev/ttyUSB0"
}
```

This specifies on which port the user can find the Crownstone USB dongle. For more information on this, take a look at the [bluenet lib](https://github.com/crownstone/bluenet-python-lib).

### Yodiwo configuration

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

This is explained over at the [Yodiwo python agent](https://github.com/crownstone/yodiwo-python-node).

## Software Installation

```
cd scripts
sudo ./install
```

You can test with `./run` in the `scripts` directory.

## Operating System Optimization 

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

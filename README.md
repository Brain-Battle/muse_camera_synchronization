# muse_camera_synchronization

A Python program that allows to synchronize recordings of Lumix cameras with Muse EEG devices. 

This repository contains:
- A "camera_control" module, which exports classes SonyControl (for controlling Sony cameras remotely) and LumixControl (for controlling Lumix cameras remotely.)
- A script "script.py" that showcases how the above classes can be used to control two cameras at the same time.
- An app.py, that has a user interface for the camera and EEG device controls; which still needs to be implemented.

## LumixControl

LumixControl class can be used to control Panasonic Lumix Sony Wi-Fi enabled cameras remotely. This module was written by [https://github.com/palmdalian](@palmdalian) and [https://github.com/johan12345](@johan12345) at GitHub.

The camera and the controlling device (i.e laptop) must be connected to the same network.

Afterwards, a LumixControl object can be constructed by passing the unique camera ip that can be found at the Wi-Fi settings of the camera.

Class uses this IP to send requests to the camera. Via requests, user can do any action they can do physically on the camera from their controlling device.

All class methods allow user to send requests with specific usages.

## SonyControl

SonyControl class can be used to control Sony Wi-Fi enabled cameras remotely. This module was written by [https://github.com/Akysens](@Akysens) at GitHub.

The camera and the controlling device (i.e laptop) must be connected to the same network.

Afterwards, a SonyControl object can be created. Users that are connecting their device to their camera for the first time can utilize the ```pair_device()``` method of the camera to connect and find the camera URL that is used to communicate.

After pairing for the first time, user should use the ```get_camera_url()``` method and note this URL down, as instead of pairing again later, they can just pass this URL directly to their control object via the ```set_camera_url()``` method.

Once the URL has been found and sorted, users can use the class methods of SonyControl device to send requests to the camera. The camera will perform the action specified in the request and return an appropriate response.
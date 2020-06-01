
<p align="center"><img width="50%" alt="TuyaMQTT logo" src="https://github.com/TradeFace/tuyamqtt/blob/development/docs/gismocaster_logo.png?raw=true"></p>
User interface to configure set up discovery messages for TuyaMQTT and Home Assistant. 

- basic light and switch types should work. 

How does it work?
---------------
GismoCaster offers a webinterface in which you can add/alter/delete devices and setup the dps properties. This configuration is written to your MQTT broker as a retain message. 
TuyaMQTT and Home Assistant are listening for these autodiscovery topics. 

<p align="center"><img alt="Network" src="https://github.com/TradeFace/tuyamqtt/blob/development/docs/network_bg.png?raw=true"></p>

Support
------------
TuyaMQTT will add support for GismoCaster in v1.1


Docs
-------------
https://github.com/TradeFace/GismoCaster/wiki




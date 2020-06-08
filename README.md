
<p align="center"><img width="50%" alt="TuyaGateway logo" src="https://raw.githubusercontent.com/wiki/TradeFace/tuyagateway/img/gismocaster_logo.png?raw=true"></p>
User interface to configure set up discovery messages for TuyaGateway and Home Assistant. 

- basic light and switch types should work. 

How does it work?
---------------
GismoCaster offers a webinterface in which you can add/alter/delete devices and setup the dps properties. This configuration is written to your MQTT broker as a retain message. 
TuyaGateway and Home Assistant are listening for these autodiscovery topics. 

<p align="center"><img alt="Network" src="https://raw.githubusercontent.com/wiki/TradeFace/tuyagateway/img/network_bg.png"></p>

Support
------------
TuyaGateway will add support for GismoCaster in v1.1


Docs
-------------
https://github.com/TradeFace/GismoCaster/wiki




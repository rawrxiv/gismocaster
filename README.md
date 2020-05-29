
<p align="center"><img alt="TuyaMQTT logo" src="https://github.com/TradeFace/tuyamqtt/blob/development/docs/gismocaster_logo.png?raw=true"></p>
User interface to configure autodiscovery for TuyaMQTT and Home Assistant. 

- basic light and switch types should work. 

How does it work?
---------------
GismoCaster offers a webinterface in which you can add/alter/delete devices and setup the dps properties. This configuration is written to your MQTT broker as a retain message. 
TuyaMQTT and Home Assistant are listening for these autodiscovery topics. 

<p align="center"><img alt="Network" src="https://github.com/TradeFace/tuyamqtt/blob/development/docs/network_bg.png?raw=true"></p>

Support
------------
TuyaMQTT will add support for GismoCaster in v1.1

Install
------
```bash
git clone https://github.com/TradeFace/gismocaster.git
cd gismocaster
make
make install
```

Run it
--------------
```bash
python3 web/manage.py runserver --noreload
```
In your browser go to http://127.0.0.1:8000/admin

- user: admin
- pass: admin

Build docker
-------
```bash
git clone https://github.com/TradeFace/gismocaster.git
cd gismocaster
make docker
```

Running Docker
------------
```bash
docker run -it --rm --name my-app gismocaster
```

Running Docker Compose
-------------
```docker
version: '3'
services:
  homeassistant:
    ports: 
      - "8123:8123"
    ...
    restart: always
    network_mode: host
  mosquitto:
    image: eclipse-mosquitto
    ...
    restart: always
    network_mode: host
  tuyamqtt:
    image: "tuyamqtt:latest"
    hostname: tuyamqtt 
    ...
    restart: always
    network_mode: host
  gismocaster:
    ports: 
      - "8000:8000"
    image: "gismocaster:latest"
    hostname: gismocaster 
    container_name: gismocaster
    working_dir: /usr/src/app    
    command: "python3 web/manage.py runserver --noreload"
    restart: always
    network_mode: host
```


Todo
----
_v1.0.0_
- watch connection MQTT and reconnect
- check settings before connection attempt
- review db model for HA config
- select preferred status command
- dev env (Black, pylint, flake)


Future development ideas
--------
- standard mappings for often used devices
- store mapping (for reuse)
- scan the network for tuya devices / key extraction
- simple frontend display state
- add location


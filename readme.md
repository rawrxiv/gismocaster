
MQTT Devices (WIP)
==============
User interface to configure autodiscovery for TuyaMQTT (and Home Assistant: WIP). 

How does it work?
---------------
MQTT devices offers a webinterface in which you can add/alter/delete devices and setup the dps properties. This configuration is written to your MQTT broker as a retain message. 
TuyaMQTT and Home Assistant are listening for these autodiscovery topics. 

```
 
MQTT Devices -> MQTT broker -> Home Assistant sets up the device                          
                            -> TuyaMQTT sets up the device
```

Support
------------
TuyaMQTT will add support for MQTT Devices in v1.1

install
------
```bash
git clone https://github.com/TradeFace/mqttdevices.git
cd mqttdevices
make
make install
```

run it
--------------
```bash
python3 web/manage.py runserver --noreload
```
In your browser goto http://127.0.0.1:8000/admin

- user: admin
- pass: admin

build docker
-------
```bash
git clone https://github.com/TradeFace/mqttdevices.git
cd mqttdevices
make docker
```

Running Docker
------------
```bash
docker run -it --rm --name my-app mqttdevices
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
    container_name: tuyamqtt   
    working_dir: /usr/src/app    
    volumes:
      - ./config:/usr/src/app/config    
    command: "python -u main.py"
    restart: always
    network_mode: host
  mqttdevices:
    image: "mqttdevices:latest"
    hostname: mqttdevices 
    container_name: mqttdevices
    working_dir: /usr/src/app    
    command: "python3 web/manage.py runserver --noreload"
    restart: always
    network_mode: host
```


todo
----
- publish ha discovery on start/save/delete
- add dpstypes to fixtures
- watch connection MQTT and reconnect
- check settings before connection attempt

Changelog
---------
- add setup.py
- clean up db fields
- rename app to just 'tuya'
- docker config example
- docker expose port
- setup auto release Pypi
- fixture for settings
- filter out id fields tuya/discovery
- on_start publish devices once retain
- watch for changes in Devices/Dps and publish
- publish tuyamqtt config retain on start/save/delete
- watch for changes in Setting and reconnect
- signals setup
- asyncio model loader
- ~~listen to discovery topics~~
- set db path
- basic setup
- user friendly admin panels
    - device show related dps items
    - option selects   
- pre populate db for dpstypes

future development ideas
--------
- scan the network for tuya devices / key extraction


db model
----------
```
settings

devices -< dps - dpstype
```

settings
-------
```
name:str
value:str
```

device
------
```
name:str
topic:str
protocol:str
deviceid:str
localkey:str
ip:str
hass_discovery:bool
```

dps
-----
```
device: int FK
key:int
value:str
via:str (tuya|mqtt)
dpstype:int FK
```

dpstype
----------
```
name:str
valuetype:str (bool, int, str)
range_min:float
range_max:float
discoverytype:str (switch|button|?)
```
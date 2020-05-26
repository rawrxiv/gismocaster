
install
------
```
git clone https://github.com/TradeFace/mqttdevices.git
cd mqttdevices
make
make install
```

run it
--------------
python3 web/manage.py runserver --noreload

build docker
-------
```
git clone https://github.com/TradeFace/mqttdevices.git
cd mqttdevices
make docker
```

Running Docker
------------
```
docker run -it --rm --name my-app mqttdevices
```


todo
----
- publish ha discovery on start/save/delete
- watch connection MQTT and reconnect

Changelog
---------
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
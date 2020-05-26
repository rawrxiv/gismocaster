
import time
import paho.mqtt.client as mqtt
import logging
import json
import asyncio

loglevel = logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(name)s] %(message)s', level=loglevel)

client = None
connected = False
models_loaded = False
models_dict = {}


def connack_string(state):

    states = [
        'Connection successful',
        'Connection refused - incorrect protocol version',
        'Connection refused - invalid client identifier',
        'Connection refused - server unavailable',
        'Connection refused - bad username or password',
        'Connection refused - not authorised'
    ]
    return states[state]


#TODO what are the types of these func params
def on_connect(client, userdata, flags, rc):

    logger.info("MQTT Connection state: %s " % (connack_string(rc)))
    connected = True        
    publish_devices()
    # listen to homeassistant auto discovery, why?
    # client.subscribe("homeassistant/#")


#TODO what are the types of these func params
def on_message(client, userdata, message):

    logger.debug("topic %s retained %s message received %s", message.topic,
                    message.retain, str(message.payload.decode("utf-8")))
    pass


def unpublish_device(deviceid:str):

    logger.debug(f"unpublish_device tuya/discovery/{deviceid}")
    client.publish(f"tuya/discovery/{deviceid}" , None, retain=True) 


def _filter_id(dictDirty:dict):

    return dict(filter(lambda elem: elem[0][-3:] != '_id' and elem[0] != 'id', dictDirty.items()))
   
def publish_hass_dps(device: dict, dps:dict):
    
    hass_id = f'{device["deviceid"]}_{dps["key"]}'
    hass_topic = f'homeassistant/{dps["dpstype"]["discoverytype"]}/{hass_id}/config'

    payload = {
        "name": device['name'],
        "cmd_t": "~command",
        "stat_t": "~state",
        "val_tpl":"{{value_json.POWER}}",
        "pl_off": models_dict['setting'].objects.get(name="ha_payload_off").value,
        "pl_on":  models_dict['setting'].objects.get(name="ha_payload_on").value,
        "avty_t":"~availability",
        "pl_avail": models_dict['setting'].objects.get(name="ha_availability_online").value,
        "pl_not_avail":  models_dict['setting'].objects.get(name="ha_availability_offline").value,
        "uniq_id": hass_id,        
        "device":{
            "identifiers":[device["deviceid"]]
        },
        "~": f'tuya/{device["deviceid"]}/{hass_id}/'
    }
  
    try:
        logger.debug(f"{hass_topic} {json.dumps(payload)}")
        client.publish(hass_topic, json.dumps(payload), retain=True)
    except Exception as ex:
        logger.exception(f"publish_hass_dps {ex}", exc_info= False)

def publish_hass(device: dict):
    """
    homeassistant/sensor/ABBD20_status/config = {
        "name":"Kitchen Left Lighting status",
        "stat_t":"~HASS_STATE",
        "avty_t":"~LWT",
        "frc_upd":true,
        "pl_avail":"Online",
        "pl_not_avail":"Offline",
        "json_attributes_topic":"~HASS_STATE",
        "unit_of_meas":" ",
        "val_tpl":"{{value_json['RSSI']}}",
        "ic":"mdi:information-outline",
        "uniq_id":"ABBD20_status",
        "device":{
            "identifiers":["ABBD20"],
            "connections":[["mac","DC:4F:22:AB:BD:20"]],
            "name":"Kitchen Left Lighting",
            "model":"Sonoff Basic",
            "sw_version":"8.1.0.2(1e06976-tasmota)",
            "manufacturer":"Tasmota"
        },
        "~":"kitchen_left_lighting/tele/"} (retained)
    """
    payload = {
        "name": f"{device['name']} status",
        "pl_off": models_dict['setting'].objects.get(name="ha_payload_off").value,
        "pl_on":  models_dict['setting'].objects.get(name="ha_payload_on").value,
        "uniq_id":f'{device["deviceid"]}_status',
        "json_attributes_topic":"~state",
        "stat_t":"~state",
        "avty_t":"~availability",
        "device":{
            "identifiers":[device["deviceid"]],
            "name": f"{device['name']}",
            "model":"TuyaMQTT",
            "sw_version":"1.0.0",
            "manufacturer":"MQTTDevices"
        },
        "~": f'tuya/{device["deviceid"]}/'
    }
    topic = f'homeassistant/sensor/{device["deviceid"]}_status/config'

    try:
        logger.debug(f"{topic} {json.dumps(payload)}")
        client.publish(topic, json.dumps(payload), retain=True)
    except Exception as ex:
        logger.exception(f"publish_hass {ex}", exc_info= False)

    for dps in device['dps']:
        publish_hass_dps(device, dps)

def publish_device(deviceid:str):

    device = models_dict['device'].objects.get(deviceid=deviceid) 
    tuya_device = _filter_id(dict(models_dict['device'].objects.filter(deviceid__startswith=deviceid).values()[0])) 

    dpss = device.dps_set.all()
    dps_list = list(dpss.values())

    tuya_device['dps'] = []
    for dps in dps_list:        
        dpstype = models_dict['dpstype'].objects.filter(id__startswith=dps['dpstype_id']).values()[0]
        dps['dpstype'] = _filter_id(dict(dpstype))
        tuya_device['dps'].append(_filter_id(dps))
    
    
    try:
        logger.debug(f"publish_device tuya/discovery/{deviceid} {json.dumps(tuya_device)}")
        client.publish(f"tuya/discovery/{deviceid}", json.dumps(tuya_device), retain=True)
    except Exception as ex:
        logger.exception(f"publish_device {ex}", exc_info= False)
    
    #TODO publish homeassistant config retain   
    publish_hass(tuya_device)


def publish_devices():

    for device in models_dict['device'].objects.values():       
        publish_device(dict(device).get('deviceid'))  


def mqtt_connect():
    global client
    try:
        client = mqtt.Client()
        # client.enable_logger()
        # TODO: check if all values are there
        client.username_pw_set(models_dict['setting'].objects.get(name="mqtt_user").value, models_dict['setting'].objects.get(name="mqtt_pass").value)
        client.connect(models_dict['setting'].objects.get(name="mqtt_host").value, int(models_dict['setting'].objects.get(name="mqtt_port").value), 60)
        client.on_connect = on_connect
        client.loop_start()
        client.on_message = on_message

    except Exception as ex:
        logger.warning('(%s) Failed to connect to MQTT Broker %s', '', ex)
        connected = False


#Hacky construction to wait for apps to be fully loaded
async def load_models(on_models: callable):   
 
        while True:
            try:
                from .models import Setting, Device, Dps, Dpstype     
                on_models({
                    'setting': Setting,
                    'device': Device,
                    'dps': Dps,
                    'dpstype': Dpstype,
                })
                return
            except Exception as ex:
                asyncio.sleep(1)
                pass


def on_models(models):  

    global models_dict
    models_dict = models


def init():

    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(load_models(on_models))        
    finally:
        event_loop.close()
    mqtt_connect()


# class MQTT():

#     def __init__(self, on_models: callable):       
#         self.on_models = on_models
 
#         while True:
#             try:
#                 from .models import Setting, Device, Dps, Dpstype     
#                 self.on_models({
#                     'setting': Setting,
#                     'device': Device,
#                     'dps': Dps,
#                     'dpstype': Dpstype,
#                 })
#                 return
#             except Exception as ex:
#                 time.sleep(1)
#                 pass

"""
def hass_discovery(self, entity):

        if entity['ip'] != '192.168.1.25':
            return

        for item in entity['attributes']['dps'].items():
            self.hass_disc_item(item)


    def hass_disc_item(self, item):
        ""
        08:56:40 MQT: kitchen_left_lighting/tele/LWT = Online (retained)
        08:56:40 MQT: kitchen_left_lighting/cmnd/POWER = 
        08:56:40 MQT: kitchen_left_lighting/tele/INFO1 = {"Module":"Sonoff Basic","Version":"8.1.0.2(1e06976-tasmota)","FallbackTopic":"cmnd/kitchen_left_lighting_fb/","GroupTopic":"sonoffs/cmnd/"}
        08:56:40 MQT: kitchen_left_lighting/tele/INFO2 = {"WebServerMode":"Admin","Hostname":"kitchen_left_lighting-7456","IPAddress":"192.168.1.34"}
        08:56:40 MQT: kitchen_left_lighting/tele/INFO3 = {"RestartReason":"Software/System restart"}
        08:56:40 MQT: kitchen_left_lighting/stat/RESULT = {"POWER":"OFF"}
        08:56:40 MQT: kitchen_left_lighting/stat/POWER = OFF
        08:56:41 MQT: homeassistant/light/ABBD20_LI_1/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_1/config = {"name":"Kitchen Left Lighting","cmd_t":"~cmnd/POWER","stat_t":"~tele/STATE","val_tpl":"{{value_json.POWER}}","pl_off":"OFF","pl_on":"ON","avty_t":"~tele/LWT","pl_avail":"Online","pl_not_avail":"Offline","uniq_id":"ABBD20_RL_1","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]]},"~":"kitchen_left_lighting/"} (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_2/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_2/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_3/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_3/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_4/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_4/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_5/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_5/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_6/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_6/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_7/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_7/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_8/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_8/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_1/config = {"name":"Kitchen Left Lighting Button1","stat_t":"~stat/BUTTON1","avty_t":"~tele/LWT","pl_avail":"Online","pl_not_avail":"Offline","uniq_id":"ABBD20_BTN_1","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]]},"~":"kitchen_left_lighting/","value_template":"{{value_json.STATE}}","pl_on":"TOGGLE","off_delay":1} (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_2/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_3/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_4/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_1/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_2/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_3/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_4/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_5/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_6/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_7/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_8/config =  (retained)
        08:56:41 MQT: homeassistant/sensor/ABBD20_status/config = {"name":"Kitchen Left Lighting status","stat_t":"~HASS_STATE","avty_t":"~LWT","frc_upd":true,"pl_avail":"Online","pl_not_avail":"Offline","json_attributes_topic":"~HASS_STATE","unit_of_meas":" ","val_tpl":"{{value_json['RSSI']}}","ic":"mdi:information-outline","uniq_id":"ABBD20_status","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]],"name":"Kitchen Left Lighting","model":"Sonoff Basic","sw_version":"8.1.0.2(1e06976-tasmota)","manufacturer":"Tasmota"},"~":"kitchen_left_lighting/tele/"} (retained)
        08:56:44 MQT: kitchen_left_lighting/tele/STATE = {"Time":"2020-05-22T08:56:44","Uptime":"0T00:00:12","UptimeSec":1
        ""

        print(item)
        device_dps = '%s_%s' % (self.entity['deviceid'], item[0])
        ""
        we have no knowledge of what the dps values actualy do at this point
        need an interface so enduser can configure
        ""
        hass_topic = 'homeassistant/%s/%s/config' % ('unknown', device_dps)

       
        payload = {
            "name": "name here",
            "cmd_t": "~command",
            "stat_t": "~state",
            "val_tpl":"{{value_json.POWER}}",
            "pl_off": self.config['General']['payload_off'],
            "pl_on": self.config['General']['payload_off'],
            "avty_t":"~availability",
            "pl_avail": self.config['General']['availability_online'],
            "pl_not_avail": self.config['General']['availability_offline'],
            "uniq_id": device_dps,
            "device":{
                "identifiers":[self.entity['deviceid']]
            },
            "~": self.mqtt_topic
        }
        print(hass_topic)
        print(payload)
"""

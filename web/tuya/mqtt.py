
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


# TODO what are the types of these func params
def on_connect(client, userdata, flags, rc):

    logger.info("MQTT Connection state: %s " % (connack_string(rc)))
    connected = True
    publish_devices()
    # listen to homeassistant auto discovery, why?
    # client.subscribe("homeassistant/#")


# TODO what are the types of these func params
def on_message(client, userdata, message):

    logger.debug("topic %s retained %s message received %s", message.topic,
                 message.retain, str(message.payload.decode("utf-8")))
    pass

def _publish(topic:str, payload_dict:dict, clear:bool=False):

    payload = json.dumps(payload_dict)
    if clear:
        payload = None

    try:
        logger.debug(f"_publish {topic} {payload}")
        client.publish(topic, payload, retain=True)
    except Exception as ex:
        logger.exception(f"_publish {ex}", exc_info=False)

def _filter_id(dictDirty: dict):

    return dict(filter(lambda elem: elem[0][-3:] != '_id' and elem[0] != 'id', dictDirty.items()))


def publish_hass_dps(device: dict, dps: dict, clear:bool=False):

    hass_id = f'{device["deviceid"]}_{dps["key"]}'
    topic = f'homeassistant/{dps["dpstype"]["discoverytype"]}/{hass_id}/config'

    payload_dict = {
        "name": device['name'],
        "cmd_t": "~command",
        "stat_t": "~state",
        "json_attributes_topic": "~attributes",
        "val_tpl": "{{value_json.POWER}}",
        "pl_off": models_dict['setting'].objects.get(name="ha_payload_off").value,
        "pl_on":  models_dict['setting'].objects.get(name="ha_payload_on").value,
        "avty_t": f'tuya/{device["deviceid"]}/availability',
        "pl_avail": models_dict['setting'].objects.get(name="ha_availability_online").value,
        "pl_not_avail":  models_dict['setting'].objects.get(name="ha_availability_offline").value,
        "uniq_id": hass_id,
        "device": {
            "identifiers": [device["deviceid"]],
            "name": f"{device['name']}",
            "model": "TuyaMQTT",
            "sw_version": "1.0.0",
            "manufacturer": "MQTTDevices"
        },
        "~": f'tuya/{device["deviceid"]}/{dps["key"]}/'
    }

    _publish(topic, payload_dict, clear)


def publish_hass(device: dict, clear:bool=False):
    
    for dps in device['dps']:
        publish_hass_dps(device, dps, clear)


def publish_device(device, clear:bool=False):

    payload_dict = _filter_id(dict(models_dict['device'].objects.filter(
        deviceid__startswith=device.deviceid).values()[0]))

    dpss = device.dps_set.all()
    dps_list = list(dpss.values())

    payload_dict['dps'] = []
    for dps in dps_list:
        dpstype = models_dict['dpstype'].objects.filter(
            id__startswith=dps['dpstype_id']).values()[0]
        dps['dpstype'] = _filter_id(dict(dpstype))
        payload_dict['dps'].append(_filter_id(dps))

    topic = f"tuya/discovery/{device.deviceid}"

    clear_tuya = clear
    if not device.tuya_discovery:
        clear_tuya = True
    _publish(topic, payload_dict, clear_tuya)

    clear_hass = clear
    if not device.hass_discovery:
        clear_hass = True
    publish_hass(payload_dict, clear_hass)


def unpublish_device(device):

    publish_device(device, True)


def publish_devices():

    for device in models_dict['device'].objects.all():        
        publish_device(device)


def mqtt_connect():
    global client
    try:
        client = mqtt.Client()
        client.enable_logger()
        # TODO: check if all values are there
        client.username_pw_set(models_dict['setting'].objects.get(
            name="mqtt_user").value, models_dict['setting'].objects.get(name="mqtt_pass").value)
        client.connect(models_dict['setting'].objects.get(name="mqtt_host").value, int(
            models_dict['setting'].objects.get(name="mqtt_port").value), 60)
        client.on_connect = on_connect
        client.loop_start()
        client.on_message = on_message

    except Exception as ex:
        logger.warning('(%s) Failed to connect to MQTT Broker %s', '', ex)
        connected = False


# Hacky construction to wait for apps to be fully loaded
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

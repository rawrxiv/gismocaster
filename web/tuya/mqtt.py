"""Connect to MQTT and send retain messages."""
import paho.mqtt.client as mqtt
import logging
import json
import asyncio

loglevel = logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s", level=loglevel
)

client = None
connected = False
models_loaded = False
models_dict = {}


def connack_string(state):

    states = [
        "Connection successful",
        "Connection refused - incorrect protocol version",
        "Connection refused - invalid client identifier",
        "Connection refused - server unavailable",
        "Connection refused - bad username or password",
        "Connection refused - not authorised",
    ]
    return states[state]


# TODO what are the types of these func params
def on_connect(client, userdata, flags, rc):

    logger.info("MQTT Connection state: %s " % (connack_string(rc)))
    connected = True
    publish_gismos()
    # client.subscribe("homeassistant/#")


# TODO what are the types of these func params
def on_message(client, userdata, message):

    logger.debug(
        "topic %s retained %s message received %s",
        message.topic,
        message.retain,
        str(message.payload.decode("utf-8")),
    )
    pass


def _publish(topic: str, payload_dict: dict, clear: bool = False, retain: bool = True):

    payload = json.dumps(payload_dict)
    if clear:
        payload = None

    try:
        logger.debug(f"_publish {topic} {payload}")
        client.publish(topic, payload, retain=retain)
    except Exception as ex:
        logger.exception(f"_publish {ex}", exc_info=False)


def _filter_id(dictDirty: dict):
    """Remove id fields from resultset."""
    return dict(
        filter(
            lambda elem: elem[0][-3:] != "_id" and elem[0] != "id", dictDirty.items()
        )
    )


def publish_hass_dp(gismo: dict, dp: dict, clear: bool = False):
    """Send retain message for Home Assistant config to broker."""
    hass_id = f'{gismo["deviceid"]}_{dp["key"]}'
    # topic = f'homeassistant/{dp["dptype"]["discoverytype"]}/{hass_id}/config'

    payload_dict = {
        "name": gismo["name"],
        "cmd_t": "~command",
        "stat_t": "~state",
        "json_attributes_topic": "~attributes",
        "val_tpl": "{{value_json.POWER}}",
        "pl_off": models_dict["setting"].objects.get(name="ha_payload_off").value,
        "pl_on": models_dict["setting"].objects.get(name="ha_payload_on").value,
        "avty_t": f'tuya/{gismo["deviceid"]}/availability',
        "pl_avail": models_dict["setting"]
        .objects.get(name="ha_availability_online")
        .value,
        "pl_not_avail": models_dict["setting"]
        .objects.get(name="ha_availability_offline")
        .value,
        "uniq_id": hass_id,
        "device": {
            "identifiers": [gismo["deviceid"]],
            "name": f"{gismo['name']}",
            "model": "TuyaMQTT",
            "sw_version": "1.0.0",
            "manufacturer": "GismoCaster",
        },
        "~": f'tuya/{gismo["deviceid"]}/{dp["key"]}/',
    }

    # _publish(topic, payload_dict, clear)


def publish_hass(gismo: dict, clear: bool = False):
    """Send retain messages for Home Assistant config to broker."""
    for dp in gismo["dp"]:
        publish_hass_dp(gismo, dp, clear)


def publish_gismo(gismo, clear: bool = False):
    """Send retain message for TuyaMQTT config to broker."""
    payload_dict = _filter_id(
        dict(
            models_dict["gismo"]
            .objects.filter(deviceid__startswith=gismo.deviceid)
            .values()[0]
        )
    )

    dps = gismo.dp_set.all()
    dp_list = list(dps.values())

    payload_dict["dp"] = []
    for dp in dp_list:
        # dptype = (
        #     models_dict["dptype"]
        #     .objects.filter(id__startswith=dp["dptype_id"])
        #     .values()[0]
        # )
        # dp["dptype"] = _filter_id(dict(dptype))
        payload_dict["dps"].append(_filter_id(dp))

    topic = f"tuya/discovery/{gismo.deviceid}"

    clear_tuya = clear
    if not gismo.tuya_discovery:
        _publish(f"tuya/{gismo.deviceid}/kill", True, False, False)
        clear_tuya = True
    _publish(topic, payload_dict, clear_tuya)

    clear_hass = clear
    if not gismo.hass_discovery:
        clear_hass = True
    publish_hass(payload_dict, clear_hass)


def unpublish_gismo(gismo):

    _publish(f"tuya/{gismo.deviceid}/kill", True, False, False)
    publish_gismo(gismo, True)


def publish_gismos():

    for gismo in models_dict["gismo"].objects.all():
        publish_gismo(gismo)


def mqtt_connect():
    """Connect to MQTT Broker."""
    global client
    try:
        client = mqtt.Client()
        client.enable_logger()

        user = models_dict["setting"].objects.get(name="mqtt_user").value
        passwd = models_dict["setting"].objects.get(name="mqtt_pass").value
        if user and passwd:
            client.username_pw_set(
                user, passwd,
            )

        host = models_dict["setting"].objects.get(name="mqtt_host").value
        if not host:
            host = "127.0.0.1"
        port = int(models_dict["setting"].objects.get(name="mqtt_port").value)
        if not port:
            port = 1883
        client.connect(
            host, port, 60,
        )
        client.on_connect = on_connect
        client.loop_start()
        client.on_message = on_message

    except Exception as ex:
        logger.warning("(%s) Failed to connect to MQTT Broker %s", "", ex)
        connected = False


# HACK: Hacky construction to wait for apps to be fully loaded
async def load_models(on_models: callable):
    """Load database models when available."""
    while True:
        try:
            from .models import Setting, Gismo, Dp, GismoModel, HAOverwrite

            on_models(
                {"setting": Setting, "gismo": Gismo, "dp": Dp, "gismomodel": GismoModel, "HAOverwrite":HAOverwrite}
            )
            return
        except Exception:
            asyncio.sleep(1)
            pass


def on_models(models):
    """Callback on models loaded."""
    global models_dict
    models_dict = models


def init():

    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(load_models(on_models))
    finally:
        event_loop.close()
    mqtt_connect()

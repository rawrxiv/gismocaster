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


def _cast_type(type_value: str, value: str):

    if type_value == "bool":
        return bool(value)
    if type_value == "int":
        return int(value)
    if type_value == "float":
        return float(value)
    return value


def publish_hass_dp(gismo: dict, dp: dict, clear: bool = False):
    """Send retain message for Home Assistant config to broker."""

    # get the gismo
    gismo_dict = dict(
        models_dict["gismo"].objects.filter(deviceid=gismo.deviceid).values()[0]
    )

    # get defaults for ha component
    ha_component = models_dict["ha_component"].objects.get(id=dp["ha_component_id"])
    ha_vars_list = list(ha_component.variables.all().values())
    payload_dict = {}

    for item in ha_vars_list:
        if not item["default_value"]:
            continue
        payload_dict[item["abbreviation"]] = _cast_type(
            item["type_value"], item["default_value"]
        )

    # get ha overwrites
    ha_overwrites = models_dict["ha_overwrite"].objects.filter(dp_id=dp["id"]).all()
    for ha_overwrite in ha_overwrites:
        payload_dict[ha_overwrite.variable.abbreviation] = _cast_type(
            ha_overwrite.variable.type_value, ha_overwrite.value
        )

    hass_id = f'{gismo_dict["deviceid"]}_{dp["key"]}'

    topic = f"homeassistant/{ha_component.technical_name}/{hass_id}/config"

    if "name" in payload_dict:
        payload_dict["name"] = dp["name"]

    payload_dict["uniq_id"] = (hass_id,)
    if "dev" in payload_dict:
        payload_dict["dev"] = (
            {
                "ids": [gismo_dict["deviceid"]],
                "name": f"{dp['name']}",
                "mdl": f"Tuya ({gismo_dict['name']})",
                "sw": "1.0.0",
                "mf": "GismoCaster",
            },
        )
    payload_dict["~"] = f'tuya/{gismo_dict["deviceid"]}/{dp["key"]}/'
    if "avty_t" in payload_dict:
        payload_dict["avty_t"] = payload_dict["avty_t"].replace(
            "~", f'tuya/{gismo_dict["deviceid"]}/'
        )

    _publish(topic, payload_dict, clear)


def publish_hass(gismo, clear: bool = False):
    """Send retain messages for Home Assistant config to broker."""


    # get the dps
    dps = list(
        models_dict["dp"].objects.filter(gismo_id=gismo.id).values()
    )

    for dp in dps:
        publish_hass_dp(gismo, dp, clear)


def publish_gismo(gismo, clear: bool = False):
    """Send retain message for TuyaMQTT config to broker."""

    # get the device
    payload_dict = _filter_id(
        dict(models_dict["gismo"].objects.filter(deviceid=gismo.deviceid).values()[0])
    )
   

    # get the dps
    dps = models_dict["dp"].objects.filter(gismo_id=gismo.id)

    payload_dict["dps"] = list(map(_filter_id, list(dps.values())))

    topic = f"tuya/discovery/{gismo.deviceid}"

    clear_tuya = clear
    if not gismo.tuya_discovery:
        _publish(f"tuya/{gismo.deviceid}/kill", True, False, False)
        clear_tuya = True
    _publish(topic, payload_dict, clear_tuya)

    clear_hass = clear
    if not gismo.ha_discovery:
        clear_hass = True
    publish_hass(gismo, clear_hass)


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
            from .models import Setting, Gismo, Dp,  HAOverwrite
            from homeassistant.models import Component, Variable

            on_models(
                {
                    "setting": Setting,
                    "gismo": Gismo,
                    "dp": Dp,
                    "ha_overwrite": HAOverwrite,
                    "ha_component": Component,
                    "ha_variables": Variable,
                }
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
